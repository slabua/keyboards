import supervisor
# import storage
# import usb_cdc
import time
import usb_hid


time.sleep(10)

supervisor.set_next_stack_limit(4096 + 4096)

# storage.disable_usb_drive()
# usb_cdc.enable(console=False, data=False)
usb_hid.enable(boot_device=1)
