from brownie import network, accounts, chain, project
import time
import warnings
from brownie import network, accounts, chain, web3
from brownie.network.contract import BrownieEnvironmentWarning
from click import secho, prompt, Choice
from brownie.network.gas.strategies import LinearScalingStrategy

p = project.load('.', name="ReplProject")
interface = p.interface



warnings.filterwarnings("ignore", category=BrownieEnvironmentWarning)

MIN_BUFFERED_ETHER = 32*8*10**18
MAX_GAS_PRICE = 100 * 10**9 

def get_account():
    return accounts.wallet_connect()


def get_lido(user=None):
    return interface.Lido("0xae7ab96520DE3A18E5e111B5EaAb095312D7fE84", owner=user)


def main():
    network.connect('mainnet')
    user = get_account()
    print(f'got walletconnect user: {user}')
    lido = get_lido(user)


    for block in chain.new_blocks():
        secho(f">>> {block.number}", dim=True)

        gas_price = web3.eth.generate_gas_price()
        print(gas_price)
        secho(f'Gas price: {gas_price/10**9} gwei')
        if gas_price > MAX_GAS_PRICE:
            continue

        isStopped = lido.isStopped()
        secho(f'Lido is stopped: {isStopped}')
        if lido.isStopped():
            continue

        bufferedEther = lido.getBufferedEther()/10**18
        secho(f'Lido\'s buffered ether: {bufferedEther}')       
        if lido.getBufferedEther()<MIN_BUFFERED_ETHER:
            pass
            #continue
        try: 
            tx = lido.depositBufferedEther(150, {'gas_price': 10000, 'from': user, 'gas_limit': 10000000, 'allow_revert': 'True' })
            secho(str(tx))
        except Exception as e:
            secho(str(e))
        
        time.sleep(120)

main()