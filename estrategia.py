from states import UpgradeSingleton

def define_best_buy(indexes_enabled: list, upgrade_singleton: UpgradeSingleton) -> int:
    best = None
    best_cpsc = 0
    for i in indexes_enabled:
        if best is None:
            best = i
            dados = upgrade_singleton.produtos[f'product{i}']
            best_cpsc = dados[0]/dados[1]
        else:
            dados = upgrade_singleton.produtos[f'product{i}'] # isso é mais eficiente que p.get_attribute('id')
            cpsc = dados[0]/dados[1]
            if cpsc > best_cpsc:
                best = i
                best_cpsc = cpsc
    return best