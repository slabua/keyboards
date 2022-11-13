import supervisor
# import storage
# import usb_cdc
import usb_hid

supervisor.set_next_stack_limit(4096 + 4096)

# storage.disable_usb_drive()
# usb_cdc.enable(console=False, data=False)
usb_hid.enable(boot_device=1)
