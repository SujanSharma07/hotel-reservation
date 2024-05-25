# paypal_config.py

import logging

import paypalrestsdk

paypalrestsdk.configure(
    {
        "mode": "sandbox",  # sandbox or live
        "client_id": "ASu4jTqFSSmm-6Pz8C-Mg9Hbxr2EIHtKUAETevZatI2onyAYuqoQFJlpym2yR2l9SEKdyZLzjeVge5GA",
        "client_secret": "EJ-6mCwqxqbz_7bGaCp3gpGanYE1KEaoQuRMUpwPXrndmVAxyXpyV95A5DQ8e2Q48Ghtv2gr3FxCU7Y_",
    }
)

logging.basicConfig(level=logging.INFO)
