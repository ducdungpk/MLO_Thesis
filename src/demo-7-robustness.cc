#include "ns3/core-module.h"
#include "ns3/network-module.h"
#include "ns3/mobility-module.h"
#include "ns3/internet-module.h"
#include "ns3/wifi-module.h"
#include "ns3/applications-module.h"
#include "ns3/flow-monitor-module.h"

using namespace ns3;

/* ===== SAFE CHANNEL MAP ===== */

uint32_t Get5GChannel(uint32_t width)
{
  if (width == 20) return 36;
  if (width == 40) return 38;
  if (width == 80) return 42;
  NS_FATAL_ERROR("width must be 20/40/80");
}

int main(int argc, char *argv[])
{
  Time::SetResolution(Time::NS);

  /* ===== PARAMETERS ===== */

  uint32_t nSta = 10;
  double simTime = 12.0;
  double appStart = 2.0;
  uint32_t packetSize = 1200;

  double offeredLoad = 40.0;
  uint32_t mode = 0;

  double speed = 0.0;
  double nakagamiM = 1.0;

  uint32_t width = 20;
  std::string mcs = "EhtMcs9";

  CommandLine cmd(__FILE__);

  cmd.AddValue("nSta","Number of STAs",nSta);
  cmd.AddValue("mode","0=full load,1=reduced load",mode);
  cmd.AddValue("speed","Mobility speed",speed);
  cmd.AddValue("nakagamiM","Nakagami m",nakagamiM);
  cmd.AddValue("offeredLoad","Load Mbps",offeredLoad);

  cmd.Parse(argc,argv);

  /* ===== NODES ===== */

  NodeContainer ap, sta;
  ap.Create(1);
  sta.Create(nSta);

  /* ===== AP MOBILITY ===== */

  MobilityHelper mobAp;

  Ptr<ListPositionAllocator> apPos = CreateObject<ListPositionAllocator>();
  apPos->Add(Vector(0,0,0));

  mobAp.SetPositionAllocator(apPos);
  mobAp.SetMobilityModel("ns3::ConstantPositionMobilityModel");

  mobAp.Install(ap);

  /* ===== STA MOBILITY ===== */

  MobilityHelper mobSta;

  Ptr<ListPositionAllocator> pos = CreateObject<ListPositionAllocator>();

  Ptr<UniformRandomVariable> uv = CreateObject<UniformRandomVariable>();

  for(uint32_t i=0;i<nSta;i++)
  {
    pos->Add(Vector(
      uv->GetValue(-15,15),
      uv->GetValue(-15,15),
      0));
  }

  mobSta.SetPositionAllocator(pos);

  if(speed == 0)
  {
    mobSta.SetMobilityModel("ns3::ConstantPositionMobilityModel");
  }
  else
  {
    mobSta.SetMobilityModel(
      "ns3::RandomWalk2dMobilityModel",
      "Bounds",RectangleValue(Rectangle(-20,20,-20,20)),
      "Speed",StringValue("ns3::ConstantRandomVariable[Constant="+std::to_string(speed)+"]"),
      "Distance",DoubleValue(5.0));
  }

  mobSta.Install(sta);

  /* ===== CHANNEL + FADING ===== */

  YansWifiChannelHelper channel = YansWifiChannelHelper::Default();

  channel.AddPropagationLoss("ns3::NakagamiPropagationLossModel",
                             "m0",DoubleValue(nakagamiM),
                             "m1",DoubleValue(nakagamiM),
                             "m2",DoubleValue(nakagamiM));

  YansWifiPhyHelper phy;
  phy.SetChannel(channel.Create());

  uint32_t ch = Get5GChannel(width);

  phy.Set("ChannelSettings",
          StringValue("{"+std::to_string(ch)+","+std::to_string(width)+",BAND_5GHZ,0}"));

  /* ===== WIFI CONFIG ===== */

  WifiHelper wifi;
  wifi.SetStandard(WIFI_STANDARD_80211be);

  wifi.SetRemoteStationManager("ns3::ConstantRateWifiManager",
                               "DataMode",StringValue(mcs),
                               "ControlMode",StringValue("EhtMcs0"));

  WifiMacHelper mac;
  Ssid ssid("wifi7");

  mac.SetType("ns3::ApWifiMac","Ssid",SsidValue(ssid));
  NetDeviceContainer apDev = wifi.Install(phy,mac,ap);

  mac.SetType("ns3::StaWifiMac",
              "Ssid",SsidValue(ssid),
              "ActiveProbing",BooleanValue(false));

  NetDeviceContainer staDev = wifi.Install(phy,mac,sta);

  /* ===== INTERNET ===== */

  InternetStackHelper internet;
  internet.Install(ap);
  internet.Install(sta);

  Ipv4AddressHelper addr;
  addr.SetBase("10.1.1.0","255.255.255.0");

  Ipv4InterfaceContainer apIf = addr.Assign(apDev);
  addr.Assign(staDev);

  /* ===== APPLICATION ===== */

  uint16_t port = 5000;

  UdpServerHelper server(port);
  server.Install(ap.Get(0)).Start(Seconds(1));

  double interval = (packetSize*8.0)/(offeredLoad*1e6);

  for(uint32_t i=0;i<nSta;i++)
  {
    UdpClientHelper client(apIf.GetAddress(0),port);

    client.SetAttribute("MaxPackets",UintegerValue(100000000));
    client.SetAttribute("Interval",TimeValue(Seconds(interval)));
    client.SetAttribute("PacketSize",UintegerValue(packetSize));

    client.Install(sta.Get(i)).Start(Seconds(appStart));
  }

  /* ===== FLOW MONITOR ===== */

  FlowMonitorHelper flowmon;
  Ptr<FlowMonitor> monitor = flowmon.InstallAll();

  Simulator::Stop(Seconds(simTime));
  Simulator::Run();

  monitor->CheckForLostPackets();

  uint64_t tx=0,rx=0,bytes=0;

  double delay=0;
  double jitter=0;

  std::vector<double> thrPerFlow;

  for(auto const &f:monitor->GetFlowStats())
  {
    tx += f.second.txPackets;
    rx += f.second.rxPackets;
    bytes += f.second.rxBytes;

    delay += f.second.delaySum.GetSeconds();
    jitter += f.second.jitterSum.GetSeconds();

    double thrFlow=(f.second.rxBytes*8.0)/((simTime-appStart)*1e6);

    thrPerFlow.push_back(thrFlow);
  }

  double active = simTime-appStart;

  double thr = (bytes*8.0)/(active*1e6);

  double loss = tx>0 ? double(tx-rx)/tx : 0;

  double avgDelay = rx>0 ? delay/rx : 0;
  double avgJitter = rx>0 ? jitter/rx : 0;

  /* ===== FAIRNESS ===== */

  double sum=0,sumSq=0;

  for(double t:thrPerFlow)
  {
    sum+=t;
    sumSq+=t*t;
  }

  double fairness = (sumSq>0) ? (sum*sum)/(thrPerFlow.size()*sumSq) : 0;

  /* ===== OUTPUT ===== */

  double totalOffered = nSta * offeredLoad;
  double efficiency = totalOffered > 0 ? thr / totalOffered : 0;

  std::cout << "RESULT,"
            << nSta << ","
            << mode << ","
            << speed << ","
            << nakagamiM << ","
            << offeredLoad << ","
            << totalOffered << ","
            << thr << ","
            << (loss * 100.0) << ","
            << (avgDelay * 1000.0) << ","
            << (avgJitter * 1000.0) << ","
            << (efficiency * 100.0) << ","
            << fairness
            << std::endl;

  Simulator::Destroy();
}