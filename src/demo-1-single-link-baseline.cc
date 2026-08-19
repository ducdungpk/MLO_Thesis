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
  Time::SetResolution (Time::NS);

  double simulationTime = 10.0;
  double appStartTime = 1.0;
  uint32_t packetSize = 1200;
  double offeredLoadMbps = 20.0;
  std::string dataMode = "EhtMcs7";
  std::string controlMode = "EhtMcs0";
  uint32_t nSta = 1;

  CommandLine cmd(__FILE__);
  cmd.AddValue("simulationTime", "Total simulation time (s)", simulationTime);
  cmd.AddValue("appStartTime", "Application start time (s)", appStartTime);
  cmd.AddValue("packetSize", "UDP packet size (bytes)", packetSize);
  cmd.AddValue("offeredLoad", "Offered load per STA (Mbps)", offeredLoadMbps);
  cmd.AddValue("dataMode", "EHT Data MCS", dataMode);
  cmd.AddValue("controlMode", "Control MCS", controlMode);
  cmd.AddValue("nSta", "Number of STAs", nSta);
  cmd.Parse(argc, argv);

  std::cout << "\n=== DEMO 1: Single-Link EHT Baseline ===\n";

  NodeContainer staNodes;
  NodeContainer apNode;
  staNodes.Create(nSta);
  apNode.Create(1);

  YansWifiChannelHelper channel = YansWifiChannelHelper::Default();
  YansWifiPhyHelper phy;
  phy.SetChannel(channel.Create());
  phy.Set("ChannelSettings", StringValue("{36,20,BAND_5GHZ,0}"));
  phy.Set("FixedPhyBand", BooleanValue(true));

  WifiHelper wifi;
  wifi.SetStandard(WIFI_STANDARD_80211be);

  wifi.SetRemoteStationManager(
      "ns3::ConstantRateWifiManager",
      "DataMode", StringValue(dataMode),
      "ControlMode", StringValue(controlMode));

  WifiMacHelper mac;
  Ssid ssid = Ssid("eht-baseline-ssid");

  mac.SetType("ns3::StaWifiMac",
              "Ssid", SsidValue(ssid),
              "ActiveProbing", BooleanValue(false));

  NetDeviceContainer staDevices = wifi.Install(phy, mac, staNodes);

  mac.SetType("ns3::ApWifiMac",
              "Ssid", SsidValue(ssid));

  NetDeviceContainer apDevice = wifi.Install(phy, mac, apNode);

  MobilityHelper mobility;
  mobility.SetMobilityModel("ns3::ConstantPositionMobilityModel");
  mobility.Install(staNodes);
  mobility.Install(apNode);

  InternetStackHelper stack;
  stack.Install(staNodes);
  stack.Install(apNode);

  Ipv4AddressHelper address;
  address.SetBase("10.1.1.0", "255.255.255.0");

  Ipv4InterfaceContainer staIf = address.Assign(staDevices);
  Ipv4InterfaceContainer apIf = address.Assign(apDevice);

  uint16_t port = 5000;

  UdpServerHelper server(port);
  ApplicationContainer serverApp = server.Install(apNode.Get(0));
  serverApp.Start(Seconds(0.0));
  serverApp.Stop(Seconds(simulationTime));

  double intervalSeconds =
      (packetSize * 8.0) / (offeredLoadMbps * 1e6);

  for (uint32_t i = 0; i < nSta; ++i)
  {
    UdpClientHelper client(apIf.GetAddress(0), port);
    client.SetAttribute("MaxPackets", UintegerValue(0));
    client.SetAttribute("Interval", TimeValue(Seconds(intervalSeconds)));
    client.SetAttribute("PacketSize", UintegerValue(packetSize));

    ApplicationContainer app = client.Install(staNodes.Get(i));
    app.Start(Seconds(appStartTime));
    app.Stop(Seconds(simulationTime));
  }

  FlowMonitorHelper flowmon;
  Ptr<FlowMonitor> monitor = flowmon.InstallAll();

  Simulator::Stop(Seconds(simulationTime));
  Simulator::Run();

  monitor->CheckForLostPackets();

  auto stats = monitor->GetFlowStats();
  double activeTime = simulationTime - appStartTime;

  uint64_t totalTxPackets = 0;
  uint64_t totalRxPackets = 0;
  uint64_t totalRxBytes = 0;

  double totalDelay = 0;
  double totalJitter = 0;

  std::vector<double> perFlowThroughput;

  for (auto const &flow : stats)
  {
    totalTxPackets += flow.second.txPackets;
    totalRxPackets += flow.second.rxPackets;
    totalRxBytes += flow.second.rxBytes;

    totalDelay += flow.second.delaySum.GetSeconds();
    totalJitter += flow.second.jitterSum.GetSeconds();

    double thr =
        (flow.second.rxBytes * 8.0) /
        (activeTime * 1e6);

    perFlowThroughput.push_back(thr);
  }

  double throughputMbps =
      (totalRxBytes * 8.0) /
      (activeTime * 1e6);

  double offeredActual =
      (totalTxPackets * packetSize * 8.0) /
      (activeTime * 1e6);

  double totalOfferedLoad =
      offeredLoadMbps * nSta;

  double lossRate = 0.0;

  if (totalTxPackets > 0)
  {
    lossRate =
        (double)(totalTxPackets - totalRxPackets) /
        totalTxPackets * 100.0;
  }

  double meanDelay = 0.0;
  double meanJitter = 0.0;

  if (totalRxPackets > 0)
  {
    meanDelay = (totalDelay / totalRxPackets) * 1000.0;
    meanJitter = (totalJitter / totalRxPackets) * 1000.0;
  }

  double efficiency = 0.0;

  if (offeredActual > 0)
  {
    efficiency =
        throughputMbps / offeredActual * 100.0;
  }

  double fairness = 1.0;

  if (!perFlowThroughput.empty())
  {
    double sum = 0;
    double sumSq = 0;

    for (double t : perFlowThroughput)
    {
      sum += t;
      sumSq += t * t;
    }

    fairness =
        (sum * sum) /
        (perFlowThroughput.size() * sumSq);
  }

  std::cout
      << "RESULT,"
      << nSta << ","
      << offeredLoadMbps << ","
      << totalOfferedLoad << ","
      << throughputMbps << ","
      << lossRate << ","
      << meanDelay << ","
      << meanJitter << ","
      << efficiency << ","
      << fairness
      << std::endl;

  Simulator::Destroy();
  return 0;
}