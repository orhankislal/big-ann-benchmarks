from neurips23.streaming.base_postgres import BaseStreamingANNPostgres

class PostgresPgVectorscale(BaseStreamingANNPostgres):
    def __init__(self, metric, index_params):
        self.name = "PostgresPgVectorscale"
        self.pg_index_method = "diskann"
        self.guc_prefix = "diskann"

        super().__init__(metric, index_params)

    # Can add support for other metrics here.
    def determine_index_op_class(self, metric):
        if metric == 'euclidean':
            return ""
        else:
            raise Exception('Invalid metric')

    # Can add support for other metrics here.
    def determine_query_op(self, metric):
        if metric == 'euclidean':
            return "<=>"
        else:
            raise Exception('Invalid metric')
