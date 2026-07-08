from dotenv import load_dotenv
import os
from azure.identity import DefaultAzureCredential
from azure.ai.textanalytics import TextAnalyticsClient

def main():
    try:
        # Clear the console
        os.system('cls' if os.name == 'nt' else 'clear')

        # Get Configuration Settings
        load_dotenv()
        foundry_endpoint = os.getenv('FOUNDRY_ENDPOINT')


        # Create client using endpoint
        credential = DefaultAzureCredential()
        ai_client = TextAnalyticsClient(endpoint=foundry_endpoint, credential=credential)

        # Analyze each text file in the reviews folder
        reviews_folder = 'reviews'
        for file_name in os.listdir(reviews_folder):
            # Read the file contents
            print('\n-------------\n' + file_name)
            text = open(os.path.join(reviews_folder, file_name), encoding='utf8').read()
            print('\n' + text)

            # Get language
            detected_language = ai_client.detect_language(documents=[text])[0]
            print('\nDetected Language: {}'.format(detected_language.primary_language.name))

            # Get entities
            entities = ai_client.recognize_entities(documents=[text])[0].entities
            for entity in entities:
                print('\t{} ({})'.format(entity.text, entity.category))


            # Get PII
            pii_results = ai_client.recognize_pii_entities(documents=[text])[0]
            pii_entities = pii_results.entities
            if len(pii_entities) > 0:
                print('\nPII:')
                for entity in pii_entities:
                    print('\t{} ({})'.format(entity.text, entity.category))
                print('Redacted Text: {}'.format(pii_results.redacted_text))


    except Exception as ex:
        print(ex)


if __name__ == "__main__":
    main()