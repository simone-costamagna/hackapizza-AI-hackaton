import os.path

DATA_FOLDER_PATH = 'data'
MENU_FOLDER_PATH = f'{DATA_FOLDER_PATH}/Menu'
MISC_FOLDER_PATH = f'{DATA_FOLDER_PATH}/Misc'
DISH_MAPPING_PATH = os.path.join(MISC_FOLDER_PATH, "dish_mapping.json")
DOMANDE_PATH = os.path.join(DATA_FOLDER_PATH, 'domande.csv')

OUTPUT_FOLDER = 'output'

OUTPUT_PREPROCESSING_FOLDER = os.path.join(OUTPUT_FOLDER, 'preprocessing')
OUTPUT_PREPROCESSING_MD_FILES_FOLDER = os.path.join(OUTPUT_PREPROCESSING_FOLDER, 'md_files')
OUTPUT_JSON_TEMPLATES_FOLDER = os.path.join(OUTPUT_PREPROCESSING_FOLDER, 'json_templates')
OUTPUT_JSON_TEMPLATE_FOLDER = os.path.join(OUTPUT_PREPROCESSING_FOLDER, 'json_template')

OUTPUT_KB_FOLDER = os.path.join(OUTPUT_FOLDER, 'kb')
OUTPUT_KB_ENTITIES_FOLDER = os.path.join(OUTPUT_KB_FOLDER, 'entities')
OUTPUT_KB_GRAPH_SCHEMA = os.path.join(OUTPUT_KB_FOLDER, 'graph_schema')
OUTPUT_KB_CHROMA = os.path.join(OUTPUT_KB_FOLDER, 'chroma')

OUTPUT_APP = os.path.join(OUTPUT_FOLDER, 'app')
OUTPUT_DOMANDE = os.path.join(OUTPUT_APP, 'output.csv')

CONTESTO = """
    Benvenuti nel Ciclo Cosmico 789, dove l'umanità ha superato non solo i confini del proprio sistema solare, ma anche
    quelli delle dimensioni conosciute. In questo vasto intreccio di realtà e culture, la gastronomia si è evoluta in
    un'arte che trascende spazio e tempo.\n
    Ristoranti di ogni tipo arricchiscono il tessuto stesso del multiverso: dai sushi bar di Pandora che servono prelibati 
    sashimi di Magikarp e ravioli al Vaporeon, alle taverne di Tatooine dove l’Erba Pipa viene utilizzata per insaporire 
    piatti prelibati, fino ai moderni locali dove lo Slurm compone salse dai sapori contrastanti - l'universo gastronomico 
    è vasto e pieno di sorprese.\n
    L'espansione galattica ha portato con sé nuove responsabilità. La Federazione Galattica monitora attentamente ogni 
    ingrediente, tecnica di preparazione e certificazione necessaria per garantire che il cibo servito sia sicuro per 
    tutte le specie senzienti. Gli chef devono destreggiarsi tra regolamenti complessi, gestire ingredienti esotici che 
    esistono simultaneamente in più stati quantici e rispettare le restrizioni alimentari di centinaia di specie 
    provenienti da ogni angolo del multiverso.\n
    Nel cuore pulsante di questo arcipelago cosmico di sapori, si erge un elemento di proporzioni titaniche, un'entità che 
    trascende la mera materialità culinaria: la Pizza Cosmica. Si narra che la sua mozzarella sia stata ricavata dalla Via 
    Lattea stessa e che, per cuocerla, sia stato necessario il calore di tre soli. Nessuno conosce le sue origini e culti 
    religiosi hanno fondato la loro fede attorno al suo mistero.\n
    La missione è sviluppare un assistente che aiuti i viaggiatori intergalattici a navigare in questo ricco panorama 
    culinario.\n
    Il sistema dovrà essere in grado di suggerire agli utenti piatti appropriati sulla base delle loro richieste:\n
    - Interpretando domande in linguaggio naturale\n
    - Gestendo query complesse che coinvolgono preferenze e restrizioni alimentari\n
    - Elaborando informazioni provenienti da diverse fonti (menu, blog post, leggi galattiche e manuali di cucina)\n
    - Verificando (qualora richiesto dalla domanda) la conformità dei piatti con le normative vigenti\n
"""
