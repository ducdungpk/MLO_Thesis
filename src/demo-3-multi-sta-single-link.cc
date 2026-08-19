#include "ns3/core-module.h"
#include "ns3/network-module.h"
#include "ns3/mobility-module.h"
#include "ns3/internet-module.h"
#include "ns3/wifi-module.h"
#include "ns3/applications-module.h"
#include "ns3/flow-monitor-module.h"

using namespace ns3;

int main (int argc, char *argv[])
{
  Time::SetResolution (Time::NS);

  /* ================= PARAMETERS ================= */
  uint32_t nSta = 10;
  double simulationTime = 10.0;
  double appStartTime = 1.0;
  uint32_t packetSize = 1200;
  double offeredLoadMbps = 20.0;
  std::string dataMode = "EhtMcs7";

  CommandLine cmd(__FILE__);
  cmd.AddValue ("nSta", "Number of STAs", nSta);
  cmd.AddValue ("offeredLoad", "Offered load per STA (Mbps)", offeredLoadMbps);
  cmd.AddValue ("packetSize", "Packet size (bytes)", packetSize);
  cmd.AddValue ("dataMode", "WiFi data mode", dataMode);
  cmd.Parse (argc, argv);

  /* ================= NODES ================= */
  NodeContainer apNode;
  NodeContainer staNodes;
  apNode.Create (1);
  staNodes.Create (nSta);

  MobilityHelper mobility;
  mobility.SetMobilityModel ("ns3::ConstantPositionMobilityModel");
  mobility.Install (apNode);
  mobility.Install (staNodes);

  /* ================= WIFI ================= */
  YansWifiChannelHelper channel = YansWifiChannelHelper::Default ();
  YansWifiPhyHelper phy;
  phy.SetChannel (channel.Create ());
  phy.Set ("ChannelSettings",
           StringValue ("{36, 20, BAND_5GHZ, 0}"));

  WifiHelper wifi;
  wifi.SetStandard (WIFI_STANDARD_80211be);
  wifi.SetRemoteStationManager ("ns3::ConstantRateWifiManager",
                                "DataMode", StringValue (dataMode),
                                "ControlMode", StringValue ("EhtMcs0"));

  WifiMacHelper mac;
  Ssid ssid = Ssid ("single-link-saturation");

  mac.SetType ("ns3::ApWifiMac",
               "Ssid", SsidValue (ssid));
  NetDeviceContainer apDev = wifi.Install (phy, mac, apNode);

  mac.SetType ("ns3::StaWifiMac",
               "Ssid", SsidValue (ssid),
               "ActiveProbing", BooleanValue (false));
  NetDeviceContainer staDevs = wifi.Install (phy, mac, staNodes);

  /* ================= INTERNET ================= */
  InternetStackHelper internet;
  internet.Install (apNode);
  internet.Install (staNodes);

  Ipv4AddressHelper addr;
  addr.SetBase ("10.1.1.0", "255.255.255.0");

  Ipv4InterfaceContainer apIf = addr.Assign (apDev);
  Ipv4InterfaceContainer staIf = addr.Assign (staDevs);

  /* ================= APPLICATIONS ================= */
  uint16_t port = 5000;

  UdpServerHelper server (port);
  ApplicationContainer serverApp = server.Install (apNode.Get (0));
  serverApp.Start (Seconds (1.0));
  serverApp.Stop (Seconds (simulationTime));

  double interval =
      (packetSize * 8.0) / (offeredLoadMbps * 1e6);

  for (uint32_t i = 0; i < nSta; ++i)
  {
    UdpClientHelper client (apIf.GetAddress (0), port);
    client.SetAttribute ("MaxPackets", UintegerValue (0));
    client.SetAttribute ("Interval", TimeValue (Seconds (interval)));
    client.SetAttribute ("PacketSize", UintegerValue (packetSize));

    ApplicationContainer app = client.Install (staNodes.Get (i));
    app.Start (Seconds (appStartTime));
    app.Stop (Seconds (simulationTime));
  }

  /* ================= FLOW MONITOR ================= */
  FlowMonitorHelper flowmon;
  Ptr<FlowMonitor> monitor = flowmon.InstallAll ();

  Simulator::Stop (Seconds (simulationTime));
  Simulator::Run ();

  monitor->CheckForLostPackets ();

  Ptr<Ipv4FlowClassifier> classifier =
      DynamicCast<Ipv4FlowClassifier> (flowmon.GetClassifier ());

  double activeTime = simulationTime - appStartTime;

  uint64_t totalTx = 0;
  uint64_t totalRx = 0;
  uint64_t totalBytes = 0;
  double delaySum = 0;
  double jitterSum = 0;

  std::vector<double> perStaThroughput;

  for (auto const &flow : monitor->GetFlowStats ())
  {
    Ipv4FlowClassifier::FiveTuple t =
        classifier->FindFlow (flow.first);

    if (t.destinationPort == port)
    {
      totalTx += flow.second.txPackets;
      totalRx += flow.second.rxPackets;
      totalBytes += flow.second.rxBytes;
      delaySum += flow.second.delaySum.GetSeconds ();
      jitterSum += flow.second.jitterSum.GetSeconds ();

      double thr =
          (flow.second.rxBytes * 8.0) / (activeTime * 1e6);

      perStaThroughput.push_back (thr);
    }
  }

  double totalThroughput =
      (totalBytes * 8.0) / (activeTime * 1e6);

  double lossRatio =
      totalTx > 0 ? (double)(totalTx - totalRx) / totalTx : 0.0;

  double avgDelay =
      totalRx > 0 ? delaySum / totalRx * 1000.0 : 0.0;

  double avgJitter =
      totalRx > 0 ? jitterSum / totalRx * 1000.0 : 0.0;

  double offeredTotal = nSta * offeredLoadMbps;

  double efficiency =
      offeredTotal > 0 ? totalThroughput / offeredTotal : 0.0;

  /* Jain Fairness */
  double fairness = 1.0;
  if (perStaThroughput.size () > 1)
  {
    double sum = 0, sqSum = 0;
    for (double x : perStaThroughput)
    {
      sum += x;
      sqSum += x * x;
    }
    fairness = (sum * sum) /
               (perStaThroughput.size () * sqSum);
  }

  /*
   * Output format only:
   * - Keep raw CSV values (no key=value) for post-processing.
   * - loss and efficiency are printed as percent values, consistent with Demo 1 and Demo 2.
   */
  std::cout << "RESULT,"
            << nSta << ","
            << offeredLoadMbps << ","
            << offeredTotal << ","
            << totalThroughput << ","
            << lossRatio * 100.0 << ","
            << avgDelay << ","
            << avgJitter << ","
            << efficiency * 100.0 << ","
            << fairness
            << std::endl;

  Simulator::Destroy ();
  return 0;
}