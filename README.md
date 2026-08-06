# 📱 .NET MAUI iOS App (Windows + Cloud CI/CD + Appetize.io / TestFlight)

A cross-platform mobile application built with **C#** and **.NET MAUI** on a **Windows machine without a Mac**.

This project uses cloud-based compilation via **GitHub Actions** (`macos-14`) to build iOS binaries, enabling instant browser-based iOS testing on Windows via **Appetize.io** (100% free, no developer account required), as well as seamless deployment to physical iPhones via **Apple TestFlight**.

---

## 🛠️ Tech Stack & Architecture

* **Framework**: C# / .NET MAUI 8.0
* **IDE**: Antigravity IDE / VS Code / Visual Studio
* **OS**: Windows (Development) & macOS Cloud Runner (Compilation)
* **CI/CD Pipeline**: GitHub Actions (`macos-14`)
* **Simulator Preview**: [Appetize.io](https://appetize.io) (Browser Streaming)
* **Physical Device Deployment**: Apple TestFlight (App Store Connect API)

---

## 🚀 Quick Start: Running & Developing Locally on Windows

You can develop, modify UI, and test app logic natively on your Windows PC using the Antigravity IDE:

### 1. Prerequisites on Windows
* **.NET 8.0 SDK** (with MAUI workload):
  ```bash
  dotnet workload install maui
  ```
* **Visual Studio 2022** (with *.NET Multi-platform App UI development* workload) or **Antigravity IDE**.

### 2. Run as Windows Desktop App (WinUI 3)
To immediately launch and test the app logic on Windows without emulators:
```bash
cd MauiTestFlightApp
dotnet build -f net8.0-windows10.0.19041.0
dotnet run -f net8.0-windows10.0.19041.0
```

### 3. Run on Android (Local Emulator or Physical Phone)
```bash
dotnet build -f net8.0-android
dotnet run -f net8.0-android
```

---

## 🌐 Phase 1: Browser-Based iOS Testing (Appetize.io)

> **No Mac or Paid Apple Developer License Required!**

Appetize.io streams an interactive iOS device directly inside your Windows browser (Chrome, Edge, Firefox).

### Step 1: Trigger Cloud Build on GitHub Actions
1. Push your repository to GitHub:
   ```bash
   git add .
   git commit -m "Scaffold .NET MAUI project and CI/CD workflow"
   git push origin main
   ```
2. Navigate to your GitHub repository in your browser.
3. Click on the **Actions** tab.
4. Select **.NET MAUI iOS Cloud Build & Appetize Simulator** and click **Run workflow**.

### Step 2: Download the Simulator Artifact
1. When the workflow run completes (~3-5 minutes), scroll down to the **Artifacts** section at the bottom of the summary page.
2. Download `MauiTestFlightApp-Simulator.zip`.

### Step 3: Stream iOS App in Browser
1. Go to [Appetize.io/upload](https://appetize.io/upload).
2. Drag and drop `MauiTestFlightApp-Simulator.zip`.
3. Appetize will generate an interactive iOS simulator iframe. You can interact with the welcome card and click the counter button directly in your web browser!

### Step 4: (Optional) Automated Appetize.io Deployment
To auto-deploy builds to Appetize on every `git push`:
1. Create a free account at [Appetize.io](https://appetize.io) and copy your **API Token** from Account Settings.
2. In your GitHub Repository, go to **Settings** > **Secrets and variables** > **Actions**.
3. Add a New Repository Secret named `APPETIZE_API_TOKEN` and paste your key.
4. The workflow will automatically upload new builds and log your streaming link.

---

## 📱 Phase 2: Deploying to Physical iPhone via TestFlight

When you are ready to test on a physical iPhone using Apple TestFlight, follow these steps:

### Prerequisites for TestFlight
* Active **Apple Developer Program** ($99/year) membership.
* An iPhone with the free **TestFlight app** installed from the App Store.

---

### Step 1: Generate App Store Connect API Keys
1. Log in to [App Store Connect](https://appstoreconnect.apple.com/).
2. Go to **Users and Access** > **Integrations** > **App Store Connect API**.
3. Click **Generate API Key** (Name: `GitHub Actions CI`, Access: `App Manager` or `Developer`).
4. Save the following:
   * **Key ID** (e.g. `2X9R3AB89L`)
   * **Issuer ID** (e.g. `69a6de70-0000-0000-0000-000000000000`)
   * Download the `.p8` key file (`AuthKey_2X9R3AB89L.p8`).

---

### Step 2: Generate Distribution Certificate (.p12) on Windows (Without a Mac)
Since you are on Windows, generate your Certificate Signing Request (CSR) using **Git Bash** or **OpenSSL**:

1. Open Git Bash on Windows and generate a private key and CSR:
   ```bash
   openssl req -new -newkey rsa:2048 -nodes -keyout ios_distribution.key -out ios_distribution.csr -subj "/emailAddress=your@email.com/CN=iOS Distribution/C=US"
   ```
2. Log in to the [Apple Developer Portal](https://developer.apple.com/account/resources/certificates/list).
3. Click **+** to add a new Certificate -> Select **Apple Distribution**.
4. Upload `ios_distribution.csr` and download the generated `distribution.cer`.
5. Convert `distribution.cer` and your private key into a `.p12` file on Windows:
   ```bash
   openssl x509 -in distribution.cer -inform DER -out distribution.pem -outform PEM
   openssl pkcs12 -export -out ios_distribution.p12 -inkey ios_distribution.key -in distribution.pem -password pass:YourStrongPassword123
   ```
6. Convert `.p12` file to Base64 for GitHub Secrets:
   ```bash
   base64 -w 0 ios_distribution.p12 > p12_base64.txt
   ```

---

### Step 3: Generate Provisioning Profile (.mobileprovision)
1. In [Apple Developer Certificates & Profiles](https://developer.apple.com/account/resources/profiles/list), click **+** to create a Profile.
2. Select **App Store** under Distribution.
3. Select your App ID (`com.companyname.mauitestflightapp`) and the Distribution Certificate created in Step 2.
4. Download `MauiTestFlightApp.mobileprovision`.
5. Convert to Base64:
   ```bash
   base64 -w 0 MauiTestFlightApp.mobileprovision > profile_base64.txt
   ```

---

### Step 4: Add GitHub Repository Secrets
Navigate to your GitHub Repo -> **Settings** > **Secrets and variables** > **Actions** -> **New repository secret**:

| Secret Name | Description / Value |
| :--- | :--- |
| `APP_STORE_ISSUER_ID` | Your App Store Connect Issuer ID |
| `APP_STORE_KEY_ID` | Your App Store Connect Key ID |
| `APP_STORE_PRIVATE_KEY` | Contents of your `.p8` private key file |
| `BUILD_CERTIFICATE_BASE64` | Contents of `p12_base64.txt` |
| `P12_PASSWORD` | Password created for `.p12` in Step 2 (`YourStrongPassword123`) |
| `BUILD_PROVISION_PROFILE_BASE64` | Contents of `profile_base64.txt` |

---

### Step 5: Enable TestFlight in Workflow File
Open `.github/workflows/ios-build.yml` in Antigravity IDE and uncomment the **Future TestFlight Deployment Workflow** section at the bottom to publish signed `.ipa` files directly to TestFlight on every push!

---

## 📂 Project Structure

```
Binary/
├── .github/
│   └── workflows/
│       └── ios-build.yml          # GitHub Actions macOS Cloud Build Pipeline
├── MauiTestFlightApp/
│   ├── App.xaml / App.xaml.cs     # Main MAUI Application Entry
│   ├── AppShell.xaml              # Shell Navigation
│   ├── MainPage.xaml              # Clean UI with Welcome Card & Counter Button
│   ├── MainPage.xaml.cs           # Counter Increment & State Logic
│   ├── MauiProgram.cs             # MAUI App Builder & Dependency Injection
│   ├── Platforms/
│   │   ├── iOS/                   # iOS Info.plist & AppDelegate
│   │   ├── Android/               # Android Manifest & MainActivity
│   │   └── Windows/               # WinUI 3 App Manifest
│   └── Resources/
│       └── Styles/                # Colors & Styles Design System
├── README.md                      # Comprehensive Guide & Documentation
└── implementation_plan.md         # Architecture & Technical Plan
```

---

## 💡 Troubleshooting & Tips

* **Build Time on Cloud**: The initial `dotnet workload install maui-ios` on GitHub Actions takes ~2-3 minutes. Subsequent builds benefit from runner caching.
* **Appetize.io Timeout**: Free Appetize.io accounts allow 100 free minutes/month.
* **Antigravity IDE**: You can modify XAML and C# files directly in Antigravity IDE. Commit and push changes to automatically trigger new cloud builds.
