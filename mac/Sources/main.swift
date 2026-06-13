import AppKit

let app = NSApplication.shared
let delegate = AppDelegate()
app.delegate = delegate
app.run()

class AppDelegate: NSObject, NSApplicationDelegate {
    private var statusItem: NSStatusItem!
    private var caffeinate: Process?
    private var isActive = false

    func applicationDidFinishLaunching(_ notification: Notification) {
        NSApp.setActivationPolicy(.accessory)
        statusItem = NSStatusBar.system.statusItem(withLength: NSStatusItem.variableLength)
        startKeepAwake()
        refreshMenu()
    }

    private func startKeepAwake() {
        guard caffeinate == nil else { return }
        let p = Process()
        p.executableURL = URL(fileURLWithPath: "/usr/bin/caffeinate")
        p.arguments = ["-d"]   // prevent display sleep
        try? p.run()
        caffeinate = p
        isActive = true
    }

    private func stopKeepAwake() {
        caffeinate?.terminate()
        caffeinate = nil
        isActive = false
    }

    @objc private func toggleKeepAwake() {
        if isActive { stopKeepAwake() } else { startKeepAwake() }
        refreshMenu()
    }

    private func refreshMenu() {
        guard let button = statusItem.button else { return }
        button.title = isActive ? "Zzz ●" : "Zzz ○"

        let menu = NSMenu()

        let toggleItem = NSMenuItem(
            title: isActive ? "Active — click to stop" : "Inactive — click to start",
            action: #selector(toggleKeepAwake),
            keyEquivalent: ""
        )
        toggleItem.target = self
        menu.addItem(toggleItem)

        menu.addItem(.separator())

        let quitItem = NSMenuItem(
            title: "Quit Zzz",
            action: #selector(NSApplication.terminate(_:)),
            keyEquivalent: "q"
        )
        menu.addItem(quitItem)

        statusItem.menu = menu
    }

    func applicationWillTerminate(_ notification: Notification) {
        caffeinate?.terminate()
    }
}
