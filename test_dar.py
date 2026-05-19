import httpx
import asyncio

API_KEY = "ZpyZ6qLwflNtS3cZp5b2NY9Yyv9kd2y9k5vCDAyJwJzIRejexOsMqItvZUabFl1lB0s9yAUxxRkiItjVlAD46jPiC97duWhVY"

async def test_endpoint():
    url = "https://services.datafordeler.dk/DAR/DAR/1/REST/adresse"
    params = {
        "username": API_KEY,
        "password": API_KEY,
        "adressebetegnelse": "Nyhavn 17"
    }
    
    async with httpx.AsyncClient() as client:
        # Prøv GraphQL også
        graphql_url = "https://services.datafordeler.dk/DAR/DAR/1/graphql"
        query = """
        {
          adresse(postnummer: "1051", vejnavn: "Nyhavn") {
            id_lokalId
            adressebetegnelse
          }
        }
        """
        
        print("Testing GraphQL...")
        try:
            res_gql = await client.post(graphql_url, json={"query": query}, auth=(API_KEY, API_KEY))
            print("GraphQL Status:", res_gql.status_code)
            print("GraphQL Response:", res_gql.text[:500])
        except Exception as e:
            print("GraphQL error:", e)

        print("\nTesting REST with DAWA equivalent DAWA endpoint via Dataforsyningen just in case...")
        dawa_url = "https://api.dataforsyningen.dk/adresser"
        try:
            res_dawa = await client.get(dawa_url, params={"q": "Nyhavn 17"})
            print("DAWA Status:", res_dawa.status_code)
            if res_dawa.status_code == 200:
                print("DAWA returned data successfully.")
        except Exception as e:
            print("DAWA error:", e)

asyncio.run(test_endpoint())
