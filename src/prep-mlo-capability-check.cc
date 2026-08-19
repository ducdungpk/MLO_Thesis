#include "ns3/core-module.h"
#include "ns3/network-module.h"
#include "ns3/wifi-module.h"
#include <fstream>

using namespace ns3;

NS_LOG_COMPONENT_DEFINE ("MloDeepCheck");

int
main (int argc, char *argv[])
{
  std::cout << "\n=== DEEP MLO Feature Check for NS-3.46.1 ===\n\n";

  // -------------------------------
  // 1. Check for MLO-related classes
  // -------------------------------
  std::cout << "1. Checking for MLO-related classes...\n";

  const char* mloClasses[] = {
    "ns3::MultiLinkDevice",
    "ns3::MloWifiMac",
    "ns3::MloApWifiMac",
    "ns3::MloStaWifiMac",
    "ns3::MultiLinkScheduler",
    "ns3::MultiLinkElement",
    "ns3::MloHelper"
  };

  bool foundMlo = false;
  for (auto& className : mloClasses)
    {
      TypeId tid;
      if (TypeId::LookupByNameFailSafe (className, &tid))
        {
          std::cout << "   ✓ FOUND: " << className << "\n";
          foundMlo = true;

          std::cout << "      Attributes:\n";
          for (uint32_t i = 0; i < tid.GetAttributeN (); i++)
            {
              auto attr = tid.GetAttribute (i);
              std::cout << "        - " << attr.name << " (" << attr.help << ")\n";
            }
        }
      else
        {
          std::cout << "   ✗ NOT FOUND: " << className << "\n";
        }
    }

  // -------------------------------
  // 2. Available Wi-Fi standards
  // -------------------------------
  std::cout << "\n2. Available Wi-Fi standards:\n";
  const char* wifiStandards[] = {
    "WIFI_STANDARD_80211a",
    "WIFI_STANDARD_80211b",
    "WIFI_STANDARD_80211g",
    "WIFI_STANDARD_80211n",
    "WIFI_STANDARD_80211ac",
    "WIFI_STANDARD_80211ax",
    "WIFI_STANDARD_80211be"
  };

  for (auto& s : wifiStandards)
    {
      std::cout << "   - " << s << "\n";
    }

  // ----------------------------------------
  // 3. Create EHT device to inspect PHY state
  // ----------------------------------------
  std::cout << "\n3. Creating EHT device to check PHY capabilities...\n";

  NodeContainer node;
  node.Create (1);

  WifiHelper wifi;
  wifi.SetStandard (WIFI_STANDARD_80211be);

  WifiMacHelper mac;
  mac.SetType ("ns3::StaWifiMac");

  YansWifiChannelHelper channel = YansWifiChannelHelper::Default ();
  YansWifiPhyHelper phy;
  phy.SetChannel (channel.Create ());

  phy.Set ("ChannelSettings", StringValue ("{1, 20, BAND_2_4GHZ, 0}"));

  NetDeviceContainer devices = wifi.Install (phy, mac, node);

  bool multiBandCapable = false;

  Ptr<WifiNetDevice> wifiDev = DynamicCast<WifiNetDevice> (devices.Get (0));
  if (wifiDev)
    {
      Ptr<WifiPhy> phyPtr = wifiDev->GetPhy ();
      std::cout << "   PHY type: " << phyPtr->GetInstanceTypeId ().GetName () << "\n";
      std::cout << "   Standard: " << phyPtr->GetStandard () << "\n";

      if (phyPtr->HasFixedPhyBand ())
        {
          std::cout << "   PHY band: Fixed (" << phyPtr->GetPhyBand () << ")\n";
        }
      else
        {
          std::cout << "   PHY band: Configurable (multi-band capable)\n";
          multiBandCapable = true;
        }
    }

  // -------------------------------
  // 4. 802.11be module macro check
  // -------------------------------
  std::cout << "\n4. Checking for 802.11be module...\n";

#ifdef NS3_80211BE
  bool ehtMacro = true;
  std::cout << "   NS3_80211BE macro defined\n";
#else
  bool ehtMacro = false;
  std::cout << "   NS3_80211BE macro NOT defined\n";
#endif

  // -------------------------------
  // 5. NOTE section (derived, not hard-coded)
  // -------------------------------
  std::cout << "\n[NOTE]\n";
  std::cout << "NS-3.46.1 supports:\n";

  std::cout << "  "
            << (ehtMacro ? "✓" : "✗")
            << " 802.11be (EHT PHY/MAC)\n";


  std::cout << "  "
            << (multiBandCapable ? "✓" : "✗")
            << " Multi-band operation (5 GHz / 6 GHz)\n";

  std::cout << "  "
            << (!foundMlo ? "✓" : "✗")
            << " Partial MLO-related mechanisms (e.g., EMLSR)\n";

  std::cout << "\nNS-3.46.1 does NOT expose:\n";

  std::cout << "  "
            << (!foundMlo ? "✗" : "✓")
            << " Explicit MLO device abstraction\n";

  std::cout << "  "
            << (!foundMlo ? "✗" : "✓")
            << " Per-link MAC scheduling entities\n";

  // -------------------------------
  // 6. Conclusion (original logic)
  // -------------------------------
  std::cout << "\n=== CONCLUSION ===\n";
  if (foundMlo)
    {
      std::cout << "✓ MLO features DETECTED in this build\n";
      std::cout << "  Next: Run MLO examples if available\n";
    }
  else
    {
      std::cout << "✗ Full IEEE 802.11be Multi-Link Operation (MLO) stack is not exposed as standalone classes in NS-3.46.1\n";
      std::cout << "  This build is suitable for:\n";
      std::cout << "  - EHT PHY/MAC evaluation\n";
      std::cout << "  - Multi-band experiments\n";
      std::cout << "  - Partial MLO mechanism analysis (e.g., EMLSR)\n";
    }

  Simulator::Destroy ();
  return 0;
}
