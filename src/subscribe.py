from client import BackendClient

class Subscribe(object):

    def __init__(self, config):
        self.config = config
        self.chain_config = self.config.get('chain')
        self.backend = BackendClient()
    

    def subscribe_chain(self):
        params = {
            "ChainId": self.chain_config.get('chain_id'),
            "OrgId": self.chain_config.get('org_id'),
            "NodeId": self.chain_config.get('node_id'),
            "UserName":self.chain_config.get('user_name'),
            "NodeRpcAddress": "{0}:{1}".format(self.chain_config.get('node_host'), self.chain_config.get('node_rpc_port')),
            "Tls": 0 if self.chain_config.get('tls') else 1,
            "TLSHostName": self.chain_config.get('tls_host_name')
            }
        res = self.backend.subscribe_chain(params)
        assert res.get('Status') == "OK", f"subscribe_chain params={params} failed res={res}"
    
    def subscribe_contract(self, params:dict):
        res = self.backend.subscribe_contract(params)
        assert res.get('Status') == "OK", f"subscribe_contract params={params} failed res={res}"

    def dispatch(self):
        try:
            self.subscribe_chain()
            for contract in self.chain_config.get('contract'):
                self.subscribe_contract({"ChainId": self.chain_config.get('chain_id'),"ContractName": contract.get('name'),"ContractVersion": contract.get('version')})
                self.subscribe_contract({"ChainId": self.chain_config.get('chain_id'),"ContractName": contract.get('name'),"ContractVersion": contract.get('version')})
        except AssertionError as e:
            print(e)
            return False
        else:
            return True
