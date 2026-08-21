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
  double offeredLoadMbps = 40.0;
  std::string dataMode = "EhtMcs7";

  CommandLine cmd(__FILE__);
  cmd.AddValue ("nSta", "Number of STAs", nSta);
  cmd.AddValue ("offeredLoad", "Offered load per STA per link (Mbps)", offeredLoadMbps);
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

  /* ================= LINK 1 (5 GHz) ================= */

  YansWifiChannelHelper ch5 = YansWifiChannelHelper::Default ();
  YansWifiPhyHelper phy5;
  phy5.SetChannel (ch5.Create ());
  phy5.Set ("ChannelSettings", StringValue ("{36,20,BAND_5GHZ,0}"));

  WifiHelper wifi5;
  wifi5.SetStandard (WIFI_STANDARD_80211be);

  wifi5.SetRemoteStationManager ("ns3::ConstantRateWifiManager",
                                 "DataMode", StringValue (dataMode),
                                 "ControlMode", StringValue ("EhtMcs0"));

  WifiMacHelper mac5;
  Ssid ssid5 ("mlo-link-5");

  mac5.SetType ("ns3::ApWifiMac",
                "Ssid", SsidValue (ssid5));

  NetDeviceContainer apDev5 =
      wifi5.Install (phy5, mac5, apNode);

  mac5.SetType ("ns3::StaWifiMac",
                "Ssid", SsidValue (ssid5),
                "ActiveProbing", BooleanValue (false));

  NetDeviceContainer staDev5 =
      wifi5.Install (phy5, mac5, staNodes);

  /* ================= LINK 2 (6 GHz) ================= */

  YansWifiChannelHelper ch6 = YansWifiChannelHelper::Default ();
  YansWifiPhyHelper phy6;
  phy6.SetChannel (ch6.Create ());
  phy6.Set ("ChannelSettings", StringValue ("{5,20,BAND_6GHZ,0}"));

  WifiHelper wifi6 = wifi5;

  WifiMacHelper mac6;
  Ssid ssid6 ("mlo-link-6");

  mac6.SetType ("ns3::ApWifiMac",
                "Ssid", SsidValue (ssid6));

  NetDeviceContainer apDev6 =
      wifi6.Install (phy6, mac6, apNode);

  mac6.SetType ("ns3::StaWifiMac",
                "Ssid", SsidValue (ssid6),
                "ActiveProbing", BooleanValue (false));

  NetDeviceContainer staDev6 =
      wifi6.Install (phy6, mac6, staNodes);

  /* ================= INTERNET ================= */

  InternetStackHelper internet;
  internet.Install (apNode);
  internet.Install (staNodes);

  Ipv4AddressHelper addr;

  addr.SetBase ("10.1.1.0", "255.255.255.0");
  Ipv4InterfaceContainer apIf5 = addr.Assign (apDev5);
  addr.Assign (staDev5);

  addr.SetBase ("10.1.2.0", "255.255.255.0");
  Ipv4InterfaceContainer apIf6 = addr.Assign (apDev6);
  addr.Assign (staDev6);

  /* ================= APPLICATIONS ================= */

  uint16_t port5 = 5000;
  uint16_t port6 = 6000;

  UdpServerHelper server5 (port5);
  UdpServerHelper server6 (port6);

  ApplicationContainer s5 = server5.Install (apNode.Get (0));
  ApplicationContainer s6 = server6.Install (apNode.Get (0));

  s5.Start (Seconds (0.0));
  s6.Start (Seconds (0.0));
  s5.Stop (Seconds (simulationTime));
  s6.Stop (Seconds (simulationTime));

  double interval =
      (packetSize * 8.0) /
      (offeredLoadMbps * 1e6);

  for (uint32_t i = 0; i < nSta; ++i)
  {
    UdpClientHelper c5 (apIf5.GetAddress (0), port5);

    c5.SetAttribute ("MaxPackets", UintegerValue (0));
    c5.SetAttribute ("Interval", TimeValue (Seconds (interval)));
    c5.SetAttribute ("PacketSize", UintegerValue (packetSize));

    UdpClientHelper c6 (apIf6.GetAddress (0), port6);

    c6.SetAttribute ("MaxPackets", UintegerValue (0));
    c6.SetAttribute ("Interval", TimeValue (Seconds (interval)));
    c6.SetAttribute ("PacketSize", UintegerValue (packetSize));

    ApplicationContainer a5 = c5.Install (staNodes.Get (i));
    ApplicationContainer a6 = c6.Install (staNodes.Get (i));

    a5.Start (Seconds (appStartTime));
    a6.Start (Seconds (appStartTime));

    a5.Stop (Seconds (simulationTime));
    a6.Stop (Seconds (simulationTime));
  }

  /* ================= FLOW MONITOR ================= */

  FlowMonitorHelper flowmon;
  Ptr<FlowMonitor> monitor = flowmon.InstallAll ();

  Simulator::Stop (Seconds (simulationTime));
  Simulator::Run ();

  monitor->CheckForLostPackets ();

  Ptr<Ipv4FlowClassifier> classifier =
      DynamicCast<Ipv4FlowClassifier> (flowmon.GetClassifier ());

  double activeTime =
      simulationTime - appStartTime;

  double thr5 = 0;
  double thr6 = 0;

  uint64_t totalTx = 0;
  uint64_t totalRx = 0;

  double delaySum = 0;
  double jitterSum = 0;

  for (auto const &flow : monitor->GetFlowStats ())
  {
    Ipv4FlowClassifier::FiveTuple t =
        classifier->FindFlow (flow.first);

    double thr =
        (flow.second.rxBytes * 8.0) /
        (activeTime * 1e6);

    if (t.destinationPort == port5) thr5 += thr;
    if (t.destinationPort == port6) thr6 += thr;

    totalTx += flow.second.txPackets;
    totalRx += flow.second.rxPackets;

    delaySum += flow.second.delaySum.GetSeconds ();
    jitterSum += flow.second.jitterSum.GetSeconds ();
  }

  double totalThr = thr5 + thr6;

  double loss =
      totalTx > 0 ?
      (double)(totalTx - totalRx) / totalTx : 0.0;

  double avgDelay =
      totalRx > 0 ?
      (delaySum / totalRx) * 1000.0 : 0.0;

  double avgJitter =
      totalRx > 0 ?
      (jitterSum / totalRx) * 1000.0 : 0.0;

  double offeredTotal =
      nSta * offeredLoadMbps * 2.0;

  double efficiency =
      offeredTotal > 0 ?
      totalThr / offeredTotal : 0.0;


  /* ================= JAIN FAIRNESS (tính trên từng STA) ================= */

  // Gom throughput theo từng STA
  std::map<Ipv4Address, double> staThroughput;

  for (auto const &flow : monitor->GetFlowStats ())
  {
    Ipv4FlowClassifier::FiveTuple t = classifier->FindFlow (flow.first);

    // Chỉ xét flow từ STA đến AP (port 5000 hoặc 6000)
    if (t.destinationPort == port5 || t.destinationPort == port6)
    {
      // Lấy địa chỉ nguồn (STA)
      Ipv4Address srcAddr = t.sourceAddress;

      // Tính throughput của flow này
      double thr = (flow.second.rxBytes * 8.0) / (activeTime * 1e6);

      // Cộng dồn vào STA tương ứng
      staThroughput[srcAddr] += thr;
    }
  }

  double fairness = 1.0;
  if (staThroughput.size () > 1)
  {
    double sum = 0, sqSum = 0;
    for (auto const &entry : staThroughput)
    {
      double x = entry.second;
      sum += x;
      sqSum += x * x;
    }
    fairness = (sum * sum) / (staThroughput.size () * sqSum);
  }

  std::cout << "RESULT,"
            << nSta << ","
            << offeredLoadMbps << ","
            << offeredTotal << ","
            << thr5 << ","
            << thr6 << ","
            << totalThr << ","
            << (loss * 100.0) << ","
            << avgDelay << ","
            << avgJitter << ","
            << (efficiency * 100.0) << ","
            << fairness
            << std::endl;

  Simulator::Destroy ();
  return 0;
}