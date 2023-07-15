import objc
import AppKit
from Quartz import *

class Notification(NSObject):

    def init(self):
        self = super(Notification, self).init()
        if self is None: return None

        self.title = ""
        self.content = ""
        self.position = (0, 0)
        self.radius = 15
        self.opacity = 0.8

        self.window = AppKit.NSWindow.alloc().initWithContentRect_styleMask_backing_defer_(
            AppKit.NSRect(AppKit.NSPoint(self.position[0], self.position[1]), AppKit.NSSize(0, 0)),
            AppKit.NSBorderlessWindowMask,
            AppKit.NSBackingStoreBuffered,
            False
        )
        self.window.setLevel_(AppKit.NSStatusWindowLevel)
        self.window.setOpaque_(False)
        self.window.setBackgroundColor_(AppKit.NSColor.clearColor())

        return self

    def show(self):
        self.window.orderFrontRegardless()

        frame = self.window.frame()
        frame.size.width = 300
        frame.size.height = 200
        x, y, w, h = frame
        AppKit.NSTimer.timerWithTimeInterval_target_selector_userInfo_repeats_(
            0.01,
            self,
            self.additional_init_,
            None,
            False,
        ).retain()

    def additional_init_(self, timer):
        self.window.setFrame_display_animate_(
            NSMakeRect(self.position[0] - self.window.frame().size.width / 2,
                       self.position[1] - self.window.frame().size.height / 2,
                       self.window.frame().size.width,
                       self.window.frame().size.height
                       ),
            True,
            True
        )
        self.window.setAlphaValue_(0.0)
        AppKit.NSAnimationContext.beginGrouping()
        AppKit.NSAnimationContext.currentContext().duration = 0.5
        self.window.animator().setAlphaValue_(self.opacity)
        AppKit.NSAnimationContext.endGrouping()

    def close(self):
        AppKit.NSAnimationContext.beginGrouping()
        AppKit.NSAnimationContext.currentContext().duration = 0.5
        self.window.animator().setAlphaValue_(0.0)
        AppKit.NSAnimationContext.endGrouping()

        AppKit.NSTimer.timerWithTimeInterval_target_selector_userInfo_repeats_(
            0.6,
            self,
            self.close_,
            None,
            False,
        ).retain()

    def close_(self, timer):
        self.window.orderOut_(None)
        self.window.close()


app = AppKit.NSApplication.sharedApplication()

notification = Notification.alloc().init()
notification.title = "标题"
notification.content = "内容"
notification.position = (500, 500)
notification.radius = 15
notification.opacity = 0.8

app.activateIgnoringOtherApps_(True)
notification.show()

app.run()

# 执行完成就结束程序
AppHelper.stopEventLoop()