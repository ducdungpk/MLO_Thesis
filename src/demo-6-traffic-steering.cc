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
  NS_FATAL_ERROR("width5 must be 20/40/80");
}

int main(int argc, char *argv[])
{
  Time::SetResolution(Time::NS);

  /* ===== PARAMETERS ===== */
  uint32_t nSta = 10;
  double simTime = 10.0;
  double appStart = 2.0;
  uint32_t packetSize = 1200;

  double offeredLoad = 20.0;   // Mbps per STA
  uint32_t mode = 0;            // 0=5GHz only,1=50/50 STA split,2=steering
  double splitRatio = 0.5;

  uint32_t width5 = 20;
  std::string mcs5 = "EhtMcs7";
  std::string mcs6 = "EhtMcs7";

  CommandLine cmd(__FILE__);
  cmd.AddValue("nSta","Number of STAs",nSta);
  cmd.AddValue("mode","0=5GHz only,1=50/50 split,2=steering",mode);
  cmd.AddValue("splitRatio","Traffic ratio to 5GHz",splitRatio);
  cmd.AddValue("offeredLoad","Load per STA",offeredLoad);
  cmd.AddValue("width5","5GHz width",width5);
  cmd.Parse(argc,argv);

  /* ===== NODES ===== */
  NodeContainer ap,sta;
  ap.Create(1);
  sta.Create(nSta);

  /* ===== MOBILITY (spread STAs) ===== */
  MobilityHelper mobility;
  Ptr<ListPositionAllocator> pos = CreateObject<ListPositionAllocator>();

  pos->Add(Vector(0,0,0)); // AP

  for(uint32_t i=0;i<nSta;i++)
  {
      pos->Add(Vector(2*i,0,0));
  }

  mobility.SetPositionAllocator(pos);
  mobility.SetMobilityModel("ns3::ConstantPositionMobilityModel");
  mobility.Install(ap);
  mobility.Install(sta);

  /* ===== LINK 5GHz ===== */
  YansWifiChannelHelper ch5 = YansWifiChannelHelper::Default();
  YansWifiPhyHelper phy5;
  phy5.SetChannel(ch5.Create());

  uint32_t ch5num = Get5GChannel(width5);

  phy5.Set("ChannelSettings",
      StringValue("{" + std::to_string(ch5num) + "," +
      std::to_string(width5) + ",BAND_5GHZ,0}"));

  WifiHelper wifi5;
  wifi5.SetStandard(WIFI_STANDARD_80211be);
  wifi5.SetRemoteStationManager("ns3::ConstantRateWifiManager",
      "DataMode",StringValue(mcs5),
      "ControlMode",StringValue("EhtMcs0"));

  WifiMacHelper mac5;
  Ssid ssid5("link5");

  mac5.SetType("ns3::ApWifiMac","Ssid",SsidValue(ssid5));
  NetDeviceContainer apDev5 = wifi5.Install(phy5,mac5,ap);

  mac5.SetType("ns3::StaWifiMac",
               "Ssid",SsidValue(ssid5),
               "ActiveProbing",BooleanValue(false));

  NetDeviceContainer staDev5 = wifi5.Install(phy5,mac5,sta);

  /* ===== LINK 6GHz ===== */
  YansWifiChannelHelper ch6 = YansWifiChannelHelper::Default();
  YansWifiPhyHelper phy6;
  phy6.SetChannel(ch6.Create());

  phy6.Set("ChannelSettings",
      StringValue("{5,20,BAND_6GHZ,0}"));

  WifiHelper wifi6;
  wifi6.SetStandard(WIFI_STANDARD_80211be);
  wifi6.SetRemoteStationManager("ns3::ConstantRateWifiManager",
      "DataMode",StringValue(mcs6),
      "ControlMode",StringValue("EhtMcs0"));

  WifiMacHelper mac6;
  Ssid ssid6("link6");

  mac6.SetType("ns3::ApWifiMac","Ssid",SsidValue(ssid6));
  NetDeviceContainer apDev6 = wifi6.Install(phy6,mac6,ap);

  mac6.SetType("ns3::StaWifiMac",
               "Ssid",SsidValue(ssid6),
               "ActiveProbing",BooleanValue(false));

  NetDeviceContainer staDev6 = wifi6.Install(phy6,mac6,sta);

  /* ===== INTERNET ===== */
  InternetStackHelper internet;
  internet.Install(ap);
  internet.Install(sta);

  Ipv4AddressHelper addr;

  addr.SetBase("10.1.1.0","255.255.255.0");
  Ipv4InterfaceContainer apIf5 = addr.Assign(apDev5);
  addr.Assign(staDev5);

  addr.SetBase("10.1.2.0","255.255.255.0");
  Ipv4InterfaceContainer apIf6 = addr.Assign(apDev6);
  addr.Assign(staDev6);

  /* ===== APPLICATION ===== */

  uint16_t port5=5000;
  uint16_t port6=6000;

  UdpServerHelper server5(port5);
  UdpServerHelper server6(port6);

  server5.Install(ap.Get(0)).Start(Seconds(1));
  server6.Install(ap.Get(0)).Start(Seconds(1));

  double intervalBase =
      (packetSize*8.0)/(offeredLoad*1e6);

  for(uint32_t i=0;i<nSta;i++)
  {
      bool use5=false;
      bool use6=false;

      if(mode==0)
      {
          use5=true;
      }
      else if(mode==1)
      {
          if(i%2==0) use5=true;
          else use6=true;
      }
      else if(mode==2)
      {
          if((double)i/nSta < splitRatio)
              use5=true;
          else
              use6=true;
      }

      if(use5)
      {
          UdpClientHelper c5(apIf5.GetAddress(0),port5);
          c5.SetAttribute("MaxPackets",UintegerValue(0));
          c5.SetAttribute("Interval",TimeValue(Seconds(intervalBase)));
          c5.SetAttribute("PacketSize",UintegerValue(packetSize));

          c5.Install(sta.Get(i)).Start(Seconds(appStart));
      }

      if(use6)
      {
          UdpClientHelper c6(apIf6.GetAddress(0),port6);
          c6.SetAttribute("MaxPackets",UintegerValue(0));
          c6.SetAttribute("Interval",TimeValue(Seconds(intervalBase)));
          c6.SetAttribute("PacketSize",UintegerValue(packetSize));

          c6.Install(sta.Get(i)).Start(Seconds(appStart));
      }
  }

  /* ===== FLOW MONITOR ===== */
  FlowMonitorHelper flowmon;
  Ptr<FlowMonitor> monitor = flowmon.InstallAll();

  Simulator::Stop(Seconds(simTime));
  Simulator::Run();

  monitor->CheckForLostPackets();

  uint64_t tx=0,rx=0;
  double delaySum=0;
  double jitterSum=0;

  double active=simTime-appStart;

  double thr5=0;
  double thr6=0;

  Ptr<Ipv4FlowClassifier> classifier =
      DynamicCast<Ipv4FlowClassifier>(flowmon.GetClassifier());

  for(auto const &f: monitor->GetFlowStats())
  {
      Ipv4FlowClassifier::FiveTuple t =
          classifier->FindFlow(f.first);

      tx += f.second.txPackets;
      rx += f.second.rxPackets;

      delaySum += f.second.delaySum.GetSeconds();
      jitterSum += f.second.jitterSum.GetSeconds();

      double thrFlow =
          (f.second.rxBytes*8.0)/(active*1e6);

      if(t.destinationPort==port5) thr5+=thrFlow;
      if(t.destinationPort==port6) thr6+=thrFlow;
  }

  double thrTotal = thr5+thr6;

  double loss = tx>0 ? double(tx-rx)/tx : 0;

  double avgDelay = rx>0 ? delaySum/rx : 0;
  double avgJitter = rx>0 ? jitterSum/rx : 0;

  double efficiency = thrTotal/(nSta*offeredLoad);

  double linkFair =
      (thrTotal*thrTotal)/
      (2*(thr5*thr5+thr6*thr6)+1e-9);

std::cout << "RESULT,"
          << mode << ","
          << splitRatio << ","
          << nSta << ","
          << offeredLoad << ","
          << (nSta * offeredLoad) << ","
          << thr5 << ","
          << thr6 << ","
          << thrTotal << ","
          << (loss * 100.0) << ","
          << (avgDelay * 1000.0) << ","
          << (avgJitter * 1000.0) << ","
          << (efficiency * 100.0) << ","
          << linkFair
          << std::endl;

  Simulator::Destroy();
  return 0;
}