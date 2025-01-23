terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "4.16.0"
    }
  }
}

provider "azurerm" {
  subscription_id = var.subscription_id
  client_id       = var.client_id
  client_secret   = var.client_secret
  tenant_id       = var.tenant_id
  features {}
}

# Create a resource group
resource "azurerm_resource_group" "rg_voting_system_data_platform" {
  name     = "rg_voting_system_data_platform"
  location = "Australia Southeast"
}

# create datalake gen 2 
resource "azurerm_storage_account" "datalakevotingplatform" {
  name                     = "datalakevotingplatform"
  resource_group_name      = azurerm_resource_group.rg_voting_system_data_platform.name
  location                 = azurerm_resource_group.rg_voting_system_data_platform.location
  account_tier             = "Standard" # Premium or Standard
  account_replication_type = "LRS"
  is_hns_enabled           = true # Support for Data Lake Gen2

  tags = {
    environment = "dev"
  }
}

# Create Azure Databricks workspace
resource "azurerm_databricks_workspace" "databricks" {
  name                = "databricks-voting-system"
  resource_group_name = azurerm_resource_group.rg_voting_system_data_platform.name
  location            = azurerm_resource_group.rg_voting_system_data_platform.location
  sku                 = "standard" # Can be "standard" or "premium"

  managed_resource_group_name = "managed-rg-databricks"

  tags = {
    environment = "dev"
  }
}

# Output the Databricks workspace URL
output "databricks_workspace_url" {
  value       = azurerm_databricks_workspace.databricks.workspace_url
  description = "The URL of the Azure Databricks workspace."
}


# Create Azure Key Vault
resource "azurerm_key_vault" "voting_system_keyvault" {
  name                       = "voting-system-keyvault"
  location                   = azurerm_resource_group.rg_voting_system_data_platform.location
  resource_group_name        = azurerm_resource_group.rg_voting_system_data_platform.name
  tenant_id                  = var.tenant_id
  soft_delete_retention_days = 7
  purge_protection_enabled   = true

  sku_name = "standard" # Use sku_name instead of sku

  tags = {
    environment = "dev"
  }
}

# Create a Key Vault secret for the storage account primary key
resource "azurerm_key_vault_secret" "datalake_account_key" {
  name         = "datalake-account-key"
  value        = azurerm_storage_account.datalakevotingplatform.primary_access_key
  key_vault_id = azurerm_key_vault.voting_system_keyvault.id
}

# Output the Key Vault URL
output "key_vault_url" {
  value       = azurerm_key_vault.voting_system_keyvault.vault_uri
  description = "The URL of the Azure Key Vault."
}

# Output the secret URL
output "key_vault_secret_url" {
  value       = azurerm_key_vault_secret.datalake_account_key.id
  description = "The URL of the secret stored in Key Vault."
}


# terraform init
# terraform plan -out main.tfplan
# terraform apply main.tfplan
