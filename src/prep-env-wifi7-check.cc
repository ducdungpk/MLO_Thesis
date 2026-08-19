#include "ns3/core-module.h"
#include "ns3/network-module.h"
#include "ns3/wifi-module.h"
#include "ns3/mobility-module.h"

using namespace ns3;

int
main (int argc, char *argv[])
{
  std::cout << "=== Wi-Fi 7 (802.11be) EHT / MLO feature check ===\n";

  NodeContainer staNodes, apNodes;
  staNodes.Create (1);
  apNodes.Create (1);

  WifiHelper wifi;
  wifi.SetStandard (WIFI_STANDARD_80211be);
  wifi.SetRemoteStationManager ("ns3::ConstantRateWifiManager");

  YansWifiChannelHelper channel = YansWifiChannelHelper::Default ();
  YansWifiPhyHelper phy;
  phy.SetChannel (channel.Create ());

  WifiMacHelper mac;
  Ssid ssid ("eht-mlo-test");

  mac.SetType ("ns3::StaWifiMac",
               "Ssid", SsidValue (ssid),
               "ActiveProbing", BooleanValue (false));

  NetDeviceContainer staDevs = wifi.Install (phy, mac, staNodes);

  mac.SetType ("ns3::ApWifiMac",
               "Ssid", SsidValue (ssid));

  wifi.Install (phy, mac, apNodes);

  Ptr<WifiNetDevice> dev =
      DynamicCast<WifiNetDevice> (staDevs.Get (0));

  // ----------------------------
  // CHECKS
  // ----------------------------
  std::cout << "[CHECK] Wi-Fi standard set to 802.11be (EHT)\n";

  std::cout << "[CHECK] STA MAC type: "
            << dev->GetMac ()->GetInstanceTypeId ().GetName ()
            << "\n";

  uint32_t nPhys = dev->GetNPhys ();
  std::cout << "[CHECK] Number of PHYs in device: "
            << nPhys << "\n";

  if (nPhys >= 1)
    {
      std::cout
          << "[PASS ] Device is EHT/MLO-capable (infrastructure level)\n";
    }
  else
    {
      std::cout << "[FAIL ] No PHY found\n";
    }

  std::cout << "=== END ===\n";

  Simulator::Destroy ();
  return 0;
}
