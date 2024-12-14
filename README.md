How to add functionality XXX:

Main classes: 
1) As done in core/help, add a new file core/xxx/xxx_message_handler.py with:
   2) XXXMessage 
   3) XXXMessageHandler 

Coordinate the creation of objects:
2) At dependency_injection/\_\_init__.py add import for xxx_bootstrap_di and call it at bootstrap_di()
    - Create xxx handler and map to TG command:
      1) At dependency_injection/bot_di.py
         1) add new_wrapped_xxx_message_handler 
         2) call it under bot_bootstrap_di()
    
    - Defines the creation for TG xxx handler: 
      2) Add a new file core/xxx/xxx_telegram_message_handler.py with a function new_wrapped_xxx_message_handler

Maps the TG xxx handler to message_type:
3) Add a new file dependency_injection/xxx_di.py with a xxx_bootstrap_di() function
