param project string
@allowed([
  'dev'
  'stg'
  'prod'
])
param env string
param location string = resourceGroup().location
param deployment_id string
param contributor_principal_id string

//https://docs.microsoft.com/en-us/azure/role-based-access-control/built-in-roles
var contributor = subscriptionResourceId('Microsoft.Authorization/roleDefinitions', 'b24988ac-6180-42a0-ab88-20f7382dd24c')

resource databricks 'Microsoft.Databricks/workspaces@2018-04-01' = {
  name: '${project}-dbw-${env}-${deployment_id}'
  location: location
  tags: {
    DisplayName: 'Databricks Workspace'
    Environment: env
  }
  sku: {
    name: 'premium'
  }
  properties: {
    managedResourceGroupId: subscriptionResourceId('Microsoft.Resources/resourceGroups', '${project}-${deployment_id}-dbw-${env}-rg')
  }
}
// access connector for external location
// Step 1. create uer assigned managed Identity

resource databricks_managed_identity_ext_loc 'Microsoft.ManagedIdentity/userAssignedIdentities@2023-07-31-preview' = {
  type: 'Microsoft.ManagedIdentity/userAssignedIdentities'
  apiVersion: '2023-07-31-preview'
  location: location
  name: '${project}-dbw-${env}-${deployment_id}'  
}



resource databricks_accessConnector_External_Loc_resource 'Microsoft.Databricks/accessConnectors@2024-05-01' = {
  name: '${project}-ac-ext-${env}-${deployment_id}'
  location: location
  identity: {
    type: 'UserAssigned'
    userAssignedIdentities: {
      '/subscriptions/334f902c-99ae-4637-9967-767272b6922c/resourcegroups/mde-ecolab-ps-dev-rg/providers/Microsoft.ManagedIdentity/userAssignedIdentities/mde-ecolab-mgdid-dev-ps': {}
    }
  }
  properties: {}
}


resource databricks_roleassignment 'Microsoft.Authorization/roleAssignments@2020-08-01-preview' = {
  name: guid(databricks.id)
  scope: databricks
  properties: {
    roleDefinitionId: contributor
    principalId: contributor_principal_id
    principalType: 'ServicePrincipal'
  }
}

output databricks_output object = databricks
output databricks_id string = databricks.id
output databricks_workspace_url string = databricks.properties.workspaceUrl
