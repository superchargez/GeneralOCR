Add-Type -TypeDefinition @"
using System;
using System.Runtime.InteropServices;

public class ScreenResolution {
    [DllImport("user32.dll")]
    internal static extern bool EnumDisplaySettings(string deviceName, int modeNum, ref DEVMODE devMode);
    [DllImport("user32.dll")]
    internal static extern int ChangeDisplaySettings(ref DEVMODE devMode, int flags);

    public struct DEVMODE {
        [MarshalAs(UnmanagedType.ByValTStr, SizeConst=32)]
        public string dmDeviceName;
        public short  dmSpecVersion;
        public short  dmDriverVersion;
        public short  dmSize;
        public short  dmDriverExtra;
        public int    dmFields;
        public int    dmPositionX;
        public int    dmPositionY;
        public ScreenOrientation dmDisplayOrientation;
        public int    dmDisplayFixedOutput;
        public short  dmColor;
        public short  dmDuplex;
        public short  dmYResolution;
        public short  dmTTOption;
        public short  dmCollate;
        [MarshalAs(UnmanagedType.ByValTStr, SizeConst = 32)]
        public string dmFormName;
        public short  dmLogPixels;
        public int    dmBitsPerPel;
        public int    dmPelsWidth;
        public int    dmPelsHeight;
        public int    dmDisplayFlags;
        public int    dmDisplayFrequency;
        public int    dmICMMethod;
        public int    dmICMIntent;
        public int    dmMediaType;
        public int    dmDitherType;
        public int    dmReserved1;
        public int    dmReserved2;
        public int    dmPanningWidth;
        public int    dmPanningHeight;
    };

    public enum ScreenOrientation : int {
        DMDO_DEFAULT = 0,
        DMDO_90 = 1,
        DMDO_180 = 2,
        DMDO_270 = 3
    }

    public static string ChangeResolution(int width, int height, int frequency) {
        DEVMODE dm = GetDevMode();
        dm.dmPelsWidth = width;
        dm.dmPelsHeight = height;
        dm.dmDisplayFrequency = frequency;

        int iRet = ChangeDisplaySettings(ref dm, 0);

        if (iRet == 0) {
            return "Screen resolution changed successfully";
        } else if (iRet == -5) {
            return "The mode test failed";
        } else if (iRet == -4) {
            return "The display driver failed the specified graphics mode";
        } else if (iRet == -3) {
            return "The mode is not supported by the display driver";
        } else if (iRet == -2) {
            return "The registry settings for the display could not be saved";
        } else {
            return "Failed to change screen resolution";
        }
    }

    private static DEVMODE GetDevMode() {
        DEVMODE dm = new DEVMODE();
        dm.dmDeviceName = new String(new char[32]);
        dm.dmFormName = new String(new char[32]);
        dm.dmSize = (short)Marshal.SizeOf(dm);
        bool modeExist = EnumDisplaySettings(null, -1, ref dm);
        return dm;
    }
}
"@

[ScreenResolution]::ChangeResolution(1600, 900, 60)
