---
name: azure-keyvault
description: Azure KeyVault secrets management
---

# Azure KeyVault

> Secure secrets management for Azure applications.

---

## ASP.NET Core Integration

```csharp
// Program.cs
var builder = WebApplication.CreateBuilder(args);

// Add KeyVault
var keyVaultName = builder.Configuration["KeyVaultName"];
var keyVaultUri = new Uri($"https://{keyVaultName}.vault.azure.net/");

builder.Configuration.AddAzureKeyVault(
    keyVaultUri,
    new DefaultAzureCredential());
```

---

## Required Package

```xml
<PackageReference Include="Azure.Extensions.AspNetCore.Configuration.Secrets" Version="1.*" />
<PackageReference Include="Azure.Identity" Version="1.*" />
```

---

## Secret Naming

```
KeyVault: ConnectionStrings--DefaultConnection
Config:   ConnectionStrings:DefaultConnection
```

Use `--` in KeyVault, maps to `:` in configuration.

---

## Access Configuration

```csharp
// Access secret like any config
var connectionString = builder.Configuration["ConnectionStrings:DefaultConnection"];
var apiKey = builder.Configuration["ExternalApi:Key"];
```

---

## Managed Identity

For Azure-hosted apps (AKS, App Service):

1. Enable Managed Identity on the resource
2. Grant KeyVault access policy to the identity
3. Use `DefaultAzureCredential()` - auto-detects

---

## Local Development

```json
// appsettings.Development.json
{
  "KeyVaultName": "my-keyvault-dev"
}
```

Use Azure CLI login: `az login`

---

## Pipeline Integration

```yaml
- task: AzureKeyVault@2
  inputs:
    azureSubscription: 'MySubscription'
    KeyVaultName: 'my-keyvault'
    SecretsFilter: 'ConnectionString,ApiKey'
```

---

## DO / DON'T

| ✅ Do | ❌ Don't |
|-------|---------|
| KeyVault for secrets | appsettings.json secrets |
| Managed Identity | Service Principal keys |
| Secret rotation | Static secrets forever |
