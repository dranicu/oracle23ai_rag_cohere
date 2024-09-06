import oci
import string
import random
import os
from zipfile import ZipFile


# Overview of Autonomous Data Warehouse
# https://docs.cloud.oracle.com/iaas/Content/Database/Concepts/adboverview.htm
# connection 
# https://docs.oracle.com/en/cloud/paas/autonomous-database/serverless/adbsb/connecting-python-mtls.html#GUID-8A38B339-72D4-4C9F-915C-0688F0F74EDE

def db_connection():
    try:
        # get signer from instance principals token
        signer = oci.auth.signers.InstancePrincipalsSecurityTokenSigner()
    except Exception:
        print("There was an error while trying to get the Signer")
        raise SystemExit
    
    # create DB wallet directory if it does not exist
    dir = "ADBWallet" 
    if not os.path.exists(dir):
        os.makedirs(dir)
    
    db_client = oci.database.DatabaseClient(config = {}, signer=signer)
    # the OCId of the ATP db from where will download the wallet
    adb_ocid = "<PLACEHOLDER>"  # ADB OCID FROM ORM STACK OR FROM YOU OCI TENANCY
    # the consumer group used wheb login to ADB
    # you can see these in tnsnames.ora
    consumer_group = "HIGH"
    #In this file will download the wallet from ATP
    dbwallet_download_zip_file = "ADBWallet/wallet.zip"
    # here will unzip the dbwallet_download_zip_file
    dbwallet_dir = "ADBWallet/atp_wallet"
    # ADB user to connect with 
    adb_user = "<PLACEHOLDER>" # ADB USER(NOT ADMIN!) FROM ORM STACK OR FROM YOU OCI ADB
    adb_pwd = "<PLACEHOLDER>" # ADB PASSWORD(NOT ADMIN!) FROM ORM STACK OR FROM YOU OCI ADB


    # generate a passwd for wallet
    atp_wallet_pwd = ''.join(random.choices(string.ascii_uppercase + string.digits, k=15)) # random string
    atp_wallet_details = oci.database.models.GenerateAutonomousDatabaseWalletDetails(password=atp_wallet_pwd)
    # will generate the wallet
    obj = db_client.generate_autonomous_database_wallet(adb_ocid, atp_wallet_details)

    # get the consumer group 
    get_autonomous_database_response = db_client.get_autonomous_database(autonomous_database_id=adb_ocid)
    for profile in get_autonomous_database_response.data.connection_strings.profiles:
        if profile.consumer_group == consumer_group:
            dns = profile.display_name
            break

    # download the wallet in dbwallet_download_zip_file
    with open(dbwallet_download_zip_file, 'w+b') as f:
        for chunk in obj.data.raw.stream(1024 * 1024, decode_content=False):
            f.write(chunk)
    # unzip the wallet in dbwallet_dir
    with ZipFile(dbwallet_download_zip_file, 'r') as zipObj:
        zipObj.extractall(dbwallet_dir)

    # Update SQLNET.ORA
    # the DIRECTORY must be set to point to location of wallet files
    with open(dbwallet_dir + '/sqlnet.ora') as orig_sqlnetora:
        newText=orig_sqlnetora.read().replace('DIRECTORY=\"?/network/admin\"', 'DIRECTORY=\"{}\"'.format(dbwallet_dir))
    with open(dbwallet_dir + '/sqlnet.ora', "w") as new_sqlnetora:
        new_sqlnetora.write(newText)



    return adb_user, adb_pwd, dns, dbwallet_dir, dbwallet_dir, atp_wallet_pwd