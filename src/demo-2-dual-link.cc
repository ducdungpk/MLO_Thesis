#include "ns3/core-module.h"
#include "ns3/network-module.h"
#include "ns3/internet-module.h"
#include "ns3/mobility-module.h"
#include "ns3/wifi-module.h"
#include "ns3/applications-module.h"
#include "ns3/flow-monitor-module.h"

using namespace ns3;

int main (int argc, char *argv[])
{
  Time::SetResolution(Time::NS);

  double simulationTime = 10.0;
  double appStartTime = 1.0;
  uint32_t packetSize = 1200;
  double offeredLoadMbps = 20.0;
  std::string dataMode = "EhtMcs7";
  std::string controlMode = "EhtMcs0";
  uint32_t nSta = 1;

  CommandLine cmd(__FILE__);
  cmd.AddValue("nSta","Number of STAs",nSta);
  cmd.AddValue("offeredLoad","Total offered load (Mbps)",offeredLoadMbps);
  cmd.Parse(argc,argv);

  std::cout << "\n=== DEMO 2: Dual Band (5GHz + 6GHz) ===\n";

  NodeContainer staNodes;
  NodeContainer apNode;

  staNodes.Create(nSta);
  apNode.Create(1);

  WifiHelper wifi;
  wifi.SetStandard(WIFI_STANDARD_80211be);

  wifi.SetRemoteStationManager(
    "ns3::ConstantRateWifiManager",
    "DataMode", StringValue(dataMode),
    "ControlMode", StringValue(controlMode));

  WifiMacHelper mac;

  /* 5 GHz */

  YansWifiChannelHelper channel5 = YansWifiChannelHelper::Default();
  YansWifiPhyHelper phy5;
  phy5.SetChannel(channel5.Create());
  phy5.Set("ChannelSettings", StringValue("{36,20,BAND_5GHZ,0}"));
  phy5.Set("FixedPhyBand", BooleanValue(true));

  Ssid ssid5("dualband-5");

  mac.SetType("ns3::StaWifiMac",
              "Ssid",SsidValue(ssid5),
              "ActiveProbing",BooleanValue(false));

  NetDeviceContainer sta5 = wifi.Install(phy5,mac,staNodes);

  mac.SetType("ns3::ApWifiMac",
              "Ssid",SsidValue(ssid5));

  NetDeviceContainer ap5 = wifi.Install(phy5,mac,apNode);

  /* 6 GHz */

  YansWifiChannelHelper channel6 = YansWifiChannelHelper::Default();
  YansWifiPhyHelper phy6;

  phy6.SetChannel(channel6.Create());
  phy6.Set("ChannelSettings",
           StringValue("{1,20,BAND_6GHZ,0}"));
  phy6.Set("FixedPhyBand", BooleanValue(true));

  Ssid ssid6("dualband-6");

  mac.SetType("ns3::StaWifiMac",
              "Ssid",SsidValue(ssid6),
              "ActiveProbing",BooleanValue(false));

  NetDeviceContainer sta6 = wifi.Install(phy6,mac,staNodes);

  mac.SetType("ns3::ApWifiMac",
              "Ssid",SsidValue(ssid6));

  NetDeviceContainer ap6 = wifi.Install(phy6,mac,apNode);

  MobilityHelper mobility;
  mobility.SetMobilityModel("ns3::ConstantPositionMobilityModel");

  mobility.Install(staNodes);
  mobility.Install(apNode);

  InternetStackHelper stack;
  stack.Install(staNodes);
  stack.Install(apNode);

  Ipv4AddressHelper address;

  address.SetBase("10.1.1.0","255.255.255.0");
  Ipv4InterfaceContainer staIf5 = address.Assign(sta5);
  Ipv4InterfaceContainer apIf5  = address.Assign(ap5);

  address.SetBase("10.2.1.0","255.255.255.0");
  Ipv4InterfaceContainer staIf6 = address.Assign(sta6);
  Ipv4InterfaceContainer apIf6  = address.Assign(ap6);

  uint16_t port5 = 5000;
  uint16_t port6 = 6000;

  UdpServerHelper server5(port5);
  UdpServerHelper server6(port6);

  auto s5 = server5.Install(apNode.Get(0));
  auto s6 = server6.Install(apNode.Get(0));

  s5.Start(Seconds(0));
  s6.Start(Seconds(0));

  s5.Stop(Seconds(simulationTime));
  s6.Stop(Seconds(simulationTime));

  /* CHIA LOAD CHO 2 BAND */

  double perLinkLoad = offeredLoadMbps / 2.0;

  double interval =
      (packetSize * 8.0) / (perLinkLoad * 1e6);

  for(uint32_t i=0;i<nSta;i++)
  {
    UdpClientHelper client5(apIf5.GetAddress(0),port5);
    client5.SetAttribute("MaxPackets",UintegerValue(0));
    client5.SetAttribute("Interval",TimeValue(Seconds(interval)));
    client5.SetAttribute("PacketSize",UintegerValue(packetSize));

    auto a5 = client5.Install(staNodes.Get(i));
    a5.Start(Seconds(appStartTime));
    a5.Stop(Seconds(simulationTime));

    UdpClientHelper client6(apIf6.GetAddress(0),port6);
    client6.SetAttribute("MaxPackets",UintegerValue(0));
    client6.SetAttribute("Interval",TimeValue(Seconds(interval)));
    client6.SetAttribute("PacketSize",UintegerValue(packetSize));

    auto a6 = client6.Install(staNodes.Get(i));
    a6.Start(Seconds(appStartTime));
    a6.Stop(Seconds(simulationTime));
  }

  FlowMonitorHelper flowmon;
  Ptr<FlowMonitor> monitor = flowmon.InstallAll();

  Simulator::Stop(Seconds(simulationTime));
  Simulator::Run();

  monitor->CheckForLostPackets();

  auto stats = monitor->GetFlowStats();
  double activeTime = simulationTime - appStartTime;

  double thr5 = 0;
  double thr6 = 0;

  double totalTxPackets = 0;
  double totalRxPackets = 0;
  double totalDelay = 0;
  double totalJitter = 0;

  Ptr<Ipv4FlowClassifier> classifier =
  DynamicCast<Ipv4FlowClassifier>(flowmon.GetClassifier());

  for(auto const &flow : stats)
  {
    totalTxPackets += flow.second.txPackets;
    totalRxPackets += flow.second.rxPackets;

    totalDelay += flow.second.delaySum.GetSeconds();
    totalJitter += flow.second.jitterSum.GetSeconds();

    double thr =
      (flow.second.rxBytes * 8.0) /
      (activeTime * 1e6);

    Ipv4FlowClassifier::FiveTuple t =
      classifier->FindFlow(flow.first);

    if(t.destinationPort == 5000) thr5 += thr;
    if(t.destinationPort == 6000) thr6 += thr;
  }

  double total = thr5 + thr6;

  double loss = 0;
  if(totalTxPackets > 0)
    loss = (1.0 - totalRxPackets/totalTxPackets) * 100.0;

  double delayMs = 0;
  if(totalRxPackets > 0)
    delayMs = (totalDelay / totalRxPackets) * 1000;

  double jitterMs = 0;
  if(totalRxPackets > 1)
    jitterMs = (totalJitter / (totalRxPackets-1)) * 1000;

  double offeredActual =
      (totalTxPackets * packetSize * 8.0) /
      (activeTime * 1e6);

  double efficiency = 0;
  if(offeredActual > 0)
    efficiency = total / offeredActual * 100;

  double fairness = 0;
  if((thr5 + thr6) > 0)
    fairness = ((thr5 + thr6)*(thr5 + thr6)) /
               (2*(thr5*thr5 + thr6*thr6));

  std::cout
  << "RESULT,"
  << nSta << ","
  << offeredActual << ","
  << thr5 << ","
  << thr6 << ","
  << total << ","
  << loss << ","
  << delayMs << ","
  << jitterMs << ","
  << efficiency << ","
  << fairness
  << std::endl;

  Simulator::Destroy();
  return 0;
}