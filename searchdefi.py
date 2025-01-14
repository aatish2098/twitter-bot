import os

from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport

def get_scanner_project(address: str, chain_id: int):
    endpoint = os.getenv("DEFI_URL")
    headers = {"X-Api-Key": os.getenv("X_API_KEY")}

    client = Client(
        transport=RequestsHTTPTransport(
            url=endpoint,
            headers=headers,
            use_json=True
        ),
        fetch_schema_from_transport=True,
    )

    query = gql(
        """
        query GetScannerProject($where: OneAddressFilter!){
             scannerProject(where: $where) {
                id
                address
                network
                inProgress
                aiScore
                contractName
                firstTxFrom
                firstTxDate
                firstTxBlock
                onChainScanned
                staticAnalizeScanned
                diffCheckScanned
                logo
                compilerVersion
                txCount
                initialFunder
                initialFunding
                outdatedCompiler
                scannedVersion
                scannerVersion
                protocol
                whitelisted
                estimatedAnalyzingTime
                rescanCount
                deploymentBlock
                sourceCodeLink
                link
                proxyData {
                    proxyOwner
                }
            }
        }
        """
    )

    params = {
        "where": {
            "address": address,  # Replace with the actual address
            "chainId": chain_id  # Replace with the actual chainId (e.g., 1 for Ethereum mainnet)
        }
    }

    response = client.execute(query, variable_values=params)
    return response.get("scannerProject", {})

def perform_holder_analysis(address: str, chain_id: int):
    endpoint = os.getenv("DEFI_URL")
    headers = {"X-Api-Key": os.getenv("X_API_KEY")}

    client = Client(
        transport=RequestsHTTPTransport(
            url=endpoint,
            headers=headers,
            use_json=True
        ),
        fetch_schema_from_transport=True,
    )

    query = gql(
        """
        query GetHolderAnalysis($where: OneAddressFilter!){
             scannerHolderAnalysis(where: $where) {
                topHolders {
                    address
                    balance
                    percent
                }
                topHoldersTotal
                topHoldersTotalPercentage
                totalHolders
                creator
                creatorBalance
                burnedPercentage
                ownerBalancePercentage
                issues{
                issues{confidence
                impact
                description
                }
                }
            }
        }
        """
    )

    params = {
        "where": {
            "address": address,  # Replace with the actual address
            "chainId": chain_id  # Replace with the actual chainId (e.g., 1 for Ethereum mainnet)
        }
    }

    response = client.execute(query, variable_values=params)
    return response.get("holderAnalysis", {})

