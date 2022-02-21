# main.py 
import index_constructor as pp
import indexing as idx


def startup(root_directory='D:/2021-2022/WINTER 2022/info_ret121/project3/WEBPAGES_RAW'):
    keywords_inverted_index = idx.InvertedIndex()
    tokens_inverted_index = idx.InvertedIndex()

    pp.run_indexer(keywords_inverted_index, tokens_inverted_index, root_directory)

    return keywords_inverted_index, tokens_inverted_index


if __name__ == '__main__':

    keywords_idx, tokens_idx = startup()
    
    engine = create_engine('postgresql://postgres:qrT90!xvnpc@localhost/htmlcorpus')
    
    query = input('Query : ')

