#include "ns3/core-module.h"
#include "ns3/network-module.h"
#include "ns3/mobility-module.h"
#include "ns3/internet-module.h"
#include "ns3/wifi-module.h"
#include "ns3/applications-module.h"
#include "ns3/flow-monitor-module.h"

using namespace ns3;

/* ===== SAFE CHANNEL MAP ===== */
uint32_t GetChannel(uint32_t band, uint32_t width)
{
  if (band == 5)
  {
    if (width == 20) return 36;
    if (width == 40) return 38;
    if (width == 80) return 42;
  }
  if (band == 6)
  {
    return 5; // safe 6 GHz
  }

  NS_FATAL_ERROR("Invalid band/width");
}

int main(int argc, char *argv[])
{
  Time::SetResolution(Time::NS);

  /* ===== PARAMETERS ===== */
  uint32_t band = 5;
  uint32_t nSta = 4;
  double offeredLoad = 10.0;   // Mbps per STA (safe default)
  uint32_t width = 20;
  std::string mcs = "EhtMcs7";
  uint32_t scenario = 0;

  double simTime = 10.0;
  double appStart = 2.0;
  uint32_t packetSize = 1400;

  CommandLine cmd(__FILE__);
  cmd.AddValue("band", "5 or 6 GHz", band);
  cmd.AddValue("nSta", "Number of STAs", nSta);
  cmd.AddValue("offeredLoad", "Offered load per STA (Mbps)", offeredLoad);
  cmd.AddValue("width", "Channel width (5GHz:20/40/80)", width);
  cmd.AddValue("mcs", "Data MCS", mcs);
  cmd.AddValue("scenario", "0=baseline,1=stress,2=realistic", scenario);
  cmd.Parse(argc, argv);

  if (band == 6)
    width = 20;

  /* ===== SCENARIO NAME ===== */
  std::string scenarioName = "baseline";
  if (scenario == 1) scenarioName = "stress";
  if (scenario == 2) scenarioName = "realistic";

  /* ===== NODES ===== */
  NodeContainer ap;
  ap.Create(1);

  NodeContainer sta;
  sta.Create(nSta);

  /* ===== WIFI ===== */
  YansWifiChannelHelper channel = YansWifiChannelHelper::Default();
  YansWifiPhyHelper phy;
  phy.SetChannel(channel.Create());

  uint32_t chNum = GetChannel(band, width);
  std::string bandStr = (band == 5) ? "BAND_5GHZ" : "BAND_6GHZ";

  phy.Set("ChannelSettings",
          StringValue("{" + std::to_string(chNum) + "," +
                      std::to_string(width) + "," +
                      bandStr + ",0}"));

  WifiHelper wifi;
  wifi.SetStandard(WIFI_STANDARD_80211be);

  wifi.SetRemoteStationManager(
      "ns3::ConstantRateWifiManager",
      "DataMode", StringValue(mcs),
      "ControlMode", StringValue("EhtMcs0"));

  WifiMacHelper mac;
  Ssid ssid("demo5");

  mac.SetType("ns3::ApWifiMac",
              "Ssid", SsidValue(ssid));

  NetDeviceContainer apDev =
      wifi.Install(phy, mac, ap);

  mac.SetType("ns3::StaWifiMac",
              "Ssid", SsidValue(ssid),
              "ActiveProbing", BooleanValue(false));

  NetDeviceContainer staDev =
      wifi.Install(phy, mac, sta);

  /* ===== MOBILITY ===== */
  MobilityHelper mobility;
  mobility.SetMobilityModel(
      "ns3::ConstantPositionMobilityModel");

  mobility.Install(ap);
  mobility.Install(sta);

  /* ===== INTERNET ===== */
  InternetStackHelper stack;
  stack.Install(ap);
  stack.Install(sta);

  Ipv4AddressHelper address;
  address.SetBase("192.168.1.0", "255.255.255.0");

  Ipv4InterfaceContainer apIf =
      address.Assign(apDev);

  address.Assign(staDev);

  /* ===== APPLICATION ===== */

  uint16_t port = 5000;

  UdpServerHelper server(port);
  server.Install(ap.Get(0))
        .Start(Seconds(1.0));

  double interval =
      (packetSize * 8.0) /
      (offeredLoad * 1e6);

  for (uint32_t i = 0; i < nSta; ++i)
  {
    UdpClientHelper client(
        apIf.GetAddress(0), port);

    client.SetAttribute("MaxPackets",
                        UintegerValue(0));

    client.SetAttribute("Interval",
                        TimeValue(Seconds(interval)));

    client.SetAttribute("PacketSize",
                        UintegerValue(packetSize));

    client.Install(sta.Get(i))
          .Start(Seconds(appStart));
  }

  /* ===== FLOW MONITOR ===== */

  FlowMonitorHelper flowmon;
  Ptr<FlowMonitor> monitor =
      flowmon.InstallAll();

  Simulator::Stop(Seconds(simTime));
  Simulator::Run();

  monitor->CheckForLostPackets();

  uint64_t tx = 0;
  uint64_t rx = 0;
  uint64_t bytes = 0;

  double delaySum = 0.0;
  double jitterSum = 0.0;

  std::vector<double> perStaThr;

  for (auto const &flow : monitor->GetFlowStats())
  {
    tx += flow.second.txPackets;
    rx += flow.second.rxPackets;
    bytes += flow.second.rxBytes;

    delaySum += flow.second.delaySum.GetSeconds();
    jitterSum += flow.second.jitterSum.GetSeconds();

    double thr =
        (flow.second.rxBytes * 8.0) /
        ((simTime - appStart) * 1e6);

    perStaThr.push_back(thr);
  }

  double active = simTime - appStart;

  double throughput =
      (bytes * 8.0) /
      (active * 1e6);

  double loss =
      tx > 0 ? double(tx - rx) / tx : 0.0;

  double delay =
      rx > 0 ? delaySum / rx : 0.0;

  double jitter =
      rx > 0 ? jitterSum / rx : 0.0;

  /* ===== FAIRNESS ===== */

  double sum = 0.0;
  double sumSq = 0.0;

  for (double x : perStaThr)
  {
    sum += x;
    sumSq += x * x;
  }

  double fairness =
      (sum * sum) /
      (nSta * sumSq + 1e-9);

  /* ===== EFFICIENCY ===== */

  double totalOffered =
      nSta * offeredLoad;

  double efficiency =
      throughput / totalOffered;

/* ===== OUTPUT ===== */

std::cout
 << "RESULT,"
 << scenarioName << ","
 << band << ","
 << nSta << ","
 << offeredLoad << ","
 << totalOffered << ","
 << width << ","
 << mcs << ","
 << throughput << ","
 << loss * 100.0 << ","
 << delay * 1000.0 << ","
 << jitter * 1000.0 << ","
 << efficiency * 100.0 << ","
 << fairness
 << std::endl;

  Simulator::Destroy();
}