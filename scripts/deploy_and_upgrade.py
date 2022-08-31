from scripts.helpful_scripts import get_account, encode_function_data, upgrade
from brownie import (
    network,
    Box,
    ProxyAdmin,
    TransparentUpgradeableProxy,
    Contract,
    BoxV2,
    config,
)


def main():
    account = get_account()
    print(f"Deploying to {network.show_active()}")
    # A) DEPLOYED
    # 1)implemented(deploying box contract)
    box = Box.deploy({"from": account})
    # 2) setting admin(proxy_admin_contract)
    proxy_admin = ProxyAdmin.deploy({"from": account})

    # initializer =box.store,1
    # 3) setting initiliazer for transparentUpgradeableProxy
    box_encode_initalizier_fuction = encode_function_data()
    # 4) upgrade (via transpare ntupgrade..contract)
    proxy = TransparentUpgradeableProxy.deploy(
        box.address,
        proxy_admin.address,
        box_encode_initalizier_fuction,
        {"from": account, "gas_limit": 1000000},
    )
    print(f"Proxy deployed to {proxy} , you can now upgrade to V2")
    # (initiliazer take box contract as initializer)(some low level python stuff to call box abi)
    proxy_box = Contract.from_abi("Box", proxy.address, Box.abi)
    proxy_box.store(2, {"from": account})
    print(proxy_box.retrieve())

    # B)UPGRADE
    box_V2 = BoxV2.deploy({"from": account})
    upgrade_transaction = upgrade(
        account, proxy, box_V2.address, proxy_admin_contract=proxy_admin
    )
    upgrade_transaction.wait(1)
    print("proxy has been upgraded")
    proxy_box = Contract.from_abi("BoxV2", proxy.address, BoxV2.abi)
    proxy_box.increament({"from": account})
    print(proxy_box.retrieve())
