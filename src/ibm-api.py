from watson_machine_learning_client import WatsonMachineLearningAPIClient

def setup():
    wml_credentials = { "apikey" : "***", 
                        "url" : "https://us-south.ml.cloud.ibm.com", 		    
                        "instance_id" : "***" 
                    }

    client = WatsonMachineLearningAPIClient( wml_credentials )
    return client

def train():
    """ Trains the clustering model """
    pass

def test():
    """ Tests the clustering model """ 
    pass

def main():
    setup()
    train()
    test()

if __name__ == "__main__":
    main()