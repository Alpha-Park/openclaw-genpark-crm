---
name: genpark-crm
description: Customer data structuring and CRM integration assistant.
version: 1.0.0
---

# genpark-crm

## Overview
This skill serves as the bridge between raw customer interactions and structured CRM architectures (such as Salesforce, Odoo, or HubSpot). It standardizes data and prepares it for sync.

## Capabilities
1. **Lead Parsing**: Extract structured lead data (Name, Company, Contact, Intent) from unstructured text or email dumps.
2. **CRM Automation Workflows**: Design triggers and automated actions for new leads or stage changes.
3. **Data Cleaning**: Identify and merge duplicate records logically.

## Usage Instructions
If a user pastes raw customer notes:
- Extract all identifiable fields into a JSON or Markdown table format.
- Categorize the lead's intent or "temperature" (Cold, Warm, Hot).
- Provide the exact API payload format or CSV structure needed to import the data into standard CRMs.
