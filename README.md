# 🛡️ api-relay-audit - Find Hidden AI Relay Risks

[![Download](https://img.shields.io/badge/Download-Visit%20Page-blue?style=for-the-badge)](https://github.com/Cheriimmunogenic168/api-relay-audit)

## 📥 Download

Use this link to visit the download page and get the app:

https://github.com/Cheriimmunogenic168/api-relay-audit

## 🖥️ What this app does

api-relay-audit is a Windows app that checks third-party AI API relay and proxy services for common security problems. It helps you spot issues such as:

- hidden prompt injection
- prompt leakage
- instruction override
- context truncation

You can use it to review how a relay handles your prompts and responses before you trust it with real work.

## ✅ Who this is for

Use this tool if you:

- send prompts through a third-party AI relay
- want to check if a proxy changes your instructions
- need to see if a service exposes private prompt content
- want a simple way to audit AI relay behavior on Windows

## 💻 System requirements

Before you install, make sure your PC has:

- Windows 10 or Windows 11
- At least 4 GB of RAM
- 200 MB of free disk space
- An internet connection for first-time setup and testing
- Permission to run downloaded apps

For the best results, use a recent Windows desktop or laptop.

## 🚀 Get the app on Windows

1. Open this page in your browser:
   https://github.com/Cheriimmunogenic168/api-relay-audit

2. Look for the latest release, download file, or install package.

3. If the app comes as a `.zip` file, save it to your Downloads folder.

4. If the app comes as an `.exe` file, download it and run it directly.

5. If Windows shows a security prompt, choose the option to keep the file only if you trust the source.

## 🧩 Install or unpack the app

### If you downloaded a ZIP file

1. Open your Downloads folder.
2. Find the `.zip` file.
3. Right-click the file.
4. Choose Extract All.
5. Pick a folder, such as Desktop or Documents.
6. Open the extracted folder.
7. Look for the app file and double-click it.

### If you downloaded an EXE file

1. Open your Downloads folder.
2. Find the `.exe` file.
3. Double-click it to start the app.
4. Follow the on-screen steps.

## 🔍 First launch

When you start api-relay-audit for the first time, it may ask for:

- a target relay or proxy URL
- a test prompt
- a scan profile
- output location for reports

If you see a settings screen, use the default values first. That gives you a clean first test.

## 🧪 How to run a basic audit

1. Open the app.
2. Enter the relay or proxy service you want to check.
3. Choose a test prompt from the built-in list or type your own.
4. Start the audit.
5. Wait for the app to send test requests and inspect the replies.
6. Read the results panel for signs of prompt injection, prompt leakage, instruction override, or truncation.

## 📄 What the results mean

The app may show findings such as:

- **Prompt injection detected**  
  The relay may be changing your input or adding hidden instructions.

- **Prompt leakage detected**  
  The service may expose system prompts, private context, or internal text.

- **Instruction override detected**  
  The relay may ignore or replace your instructions.

- **Context truncation detected**  
  The service may cut off part of the prompt or response.

- **No issue found**  
  The relay passed the test without clear signs of tampering.

## 🧰 Suggested test checks

For a full review, run more than one test. Try checks like:

- simple prompt pass-through
- system prompt exposure check
- response rewrite check
- instruction conflict check
- long prompt truncation check

This helps you see if the relay behaves the same across different cases.

## 📁 Reports and output

api-relay-audit may save results as:

- a local report file
- a log file
- a text summary
- a JSON export for later review

Keep these files in a safe folder if you plan to compare services over time.

## 🔧 Common actions

### Change the target service
Open the app settings and replace the relay or proxy URL with the one you want to test.

### Run the same test again
Use the same prompt and the same scan profile. That makes comparison easier.

### Compare two services
Run the same test on both services, then compare the report files side by side.

### Save your results
Export the report after each scan so you can review changes later.

## 🛠️ If the app will not open

If the app does not start, try these steps:

1. Right-click the app file.
2. Choose Run as administrator.
3. Check that the file is fully downloaded.
4. Move the app file to a simple folder like Desktop.
5. Try again.
6. Restart Windows and open the app once more.

## 🔐 If Windows blocks the file

If Windows shows a security message:

1. Check that you downloaded the file from the link above.
2. Open the file properties.
3. If you see an Unblock option, select it.
4. Try opening the file again.

## 🧭 Simple usage flow

1. Download the app from the link above.
2. Open it on Windows.
3. Enter the relay or proxy you want to inspect.
4. Run a scan.
5. Review the results.
6. Save the report.

## 📝 Tips for cleaner audits

- Test one relay at a time.
- Use the same prompt set for each service.
- Keep reports in dated folders.
- Review long responses for missing text.
- Check for changes after service updates.

## ❓ Common questions

### Do I need coding skills?
No. You can use the app with simple form fields and buttons.

### Can I use it on a laptop?
Yes. Any Windows laptop that meets the system requirements should work.

### Does it need a complex setup?
No. Start with the default settings, then enter the relay you want to test.

### Can I test more than one service?
Yes. Run the same audit on each relay or proxy and compare the results.

### What should I do with the report?
Keep it for your records, share it with your team, or compare it with future scans.

## 📌 Recommended first test

If you are new to api-relay-audit, start with this order:

1. use a short prompt
2. run a scan on one relay
3. read the report
4. run the same scan again
5. compare the results

This gives you a clear view of how the service handles your requests

## 🗂️ Folder setup

A simple folder layout can help you stay organized:

- `api-relay-audit`
- `scans`
- `reports`
- `logs`

Use one folder for each service if you test many relays

## 🖱️ Open the download page again

Use this link if you need to return to the app download page:

https://github.com/Cheriimmunogenic168/api-relay-audit