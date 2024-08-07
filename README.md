# Connect Address Verification Interface with watsonx Assistant

If you have a use case to verify an address, email, or telephone number, then the Address Verification Interface (AVI), powered by Loqate, is a great tool to ensure high quality data from your customers.  This guide will walk you through how to connect the AVI service to watsonx Assistant.  It will also show how to create an action within the Assistant that will ask for an address and call out to the AVI returning the Address and the quality of it.

Let's get started!

## Prerequisites

* [ibmcloud cli installed locally](https://cloud.ibm.com/docs/cli?topic=cli-install-ibmcloud-cli)
* [ibmcloud code engine plugin installed](https://cloud.ibm.com/docs/cli?topic=cli-plug-ins#cli-install-plugin)
* [watsonx Assistant service available](https://cloud.ibm.com/catalog/services/watsonx-assistant)

## Create a Code Engine Function to authenticate the service

This section is informational as a Function has been written and deployed for testing and proofs of concept.  If you plan to deploy the Assistant in a private environment, follow the steps below to deploy the function.

1. The code for the Code Engine function is available pubically on github.  Use the following command to clone it.

   ``` bash
   git clone https://github.com/ch0pper1/avi-assistant.git
   cd avi-assistant
   ```

2. Now that the code is available, login to the IBM cloud via the CLI.  There are several methods for this, which are listed [here](https://cloud.ibm.com/docs/cli?topic=cli-ibmcloud_cli#ibmcloud_login).  During the login process, you may be asked to select an account.  Choose the appropriate one that provides *Editor* rights for Code Engine projects.
3. If this is the first time working with Code Engine, a new project will need to be created.  To do this, a *Resource Group* and *Region* must first be selected.  Use the following commands to select a resource group and region.  This example selects the **watsonx** resource group and the **us-south** region, then creates an **avi** Code Engine project.

   ``` bash
   ibmcloud target -r us-south -g watsonx
   ibmcloud ce project create --name avi
   ```

   If there is an existing project that will be used, run this command:

   ``` bash
   ibmcloud ce project select --name <proj_name>
   ```

4. Now that the environment is ready, the function code can be created.  This project uses a Code Engine Function since it does not need to be run at all times.  More information on Code Engine Functions can be found [here](https://cloud.ibm.com/docs/codeengine?topic=codeengine-fun-work).

   Run the command below to deploy the function with the necessary requirements.

   ``` bash
   ibmcloud ce fn create --name avi-authorization --runtime python-3.11 --build-source .
   ```

   Once complete, verify that the function has been deployed using the command: 

   ``` bash
   ibmcloud ce function get -n avi-authorization
   ```

   Verify that the status has a value of **Ready**.

## Create and Configure watsonx Assistant

With the Authorization code running, this section will describe how to create an assistant and install a custom extension to connect to AVI.  This guide also assumes that there is a watsonx Assistant service available and you have permissions to create a new assistant.

1. Open the watsonx Assistant available to you and create a new Assistant.  If this a new Assistant service, the *Create a new assistant* dialog will be showing upon login.  Otherwise, create a new assistant with the *Create New +* option in the selector on the top bar.

   ![Create Assistant](./assets/images/create_assistant.png)

2. A [Custom Extension](https://cloud.ibm.com/docs/watson-assistant?topic=watson-assistant-add-custom-extension) will be used to connect watsonx Assistant to AVI for address verification.  To add a custom extenstion, first go to the **Integrations** section of the Assistant.
   1. From the Integrations section, scroll down and select **Build custom extension**.  This will open a dialog to import the openapi specification provided below.
      [OpenAPI spec for AVI](./assets/assistant-json/openapi_avi.json)
   2. In the Basic information, provide a name and description.  It is recommended to use the name **AVI** as this will make the next steps easier.  Click Next.
   3. Upload the OpenAPI spec downloaded from above, then click Next.
   4. A review of the specification will be displayed.  It should look similar to the below screenshot.  Click Finish.
      ![Custom Extension Review](./assets/images/custom_extension_review.png)
   5. Once the Custom Extension has been uploaded to the Assistant, credentials will need to be provided.  To do this, click on the *Add +* button on the newly created **AVI** tile.  Select Add to go into the dialog, then select Next to go into the *Authorization* section.
   6. Change the Authorization type to **OAuth 2.0**.  Provide your username and password for authenticating the AVI service in required fields as well as the  URL for your AVI service.  Select Next then Finish.
      ![Custom Extension Authorization](./assets/images/custom_extension_auth.png)

3. Now that the custom extension is in place, it is time to import an address verification Action into the assistant.  Download the Action below.
   [Download Assistant Action](./assets/assistant-json/AVI-action.json)
4. In the Assistant UI, navigate to **Actions**.  There will be a gear icon in the upper right corner of the screen for global settings.  Open this window and click on the *Upload/Download* tab.  Upload the AVI-action.json file to this window and select Upload.  
   > **Warning**  
   > This will replace all data in the Assistant, so ensure that the correct Assistant is selected.
5. 

## Use the Preview to verify an address

1. Login to the Assistant that you setup in the previous section.
2. Go to the Preview Section
3. Start a chat with the utterance "Verify address"
4. The Assistant will prompt you asking for an address to verify.  Enter the requested address.
5. The Assistant will return the verified address or suggest an update.
