# Robust Requirements & Data Model Recommendations

Based on a deep analysis of the SQL schema (`Tables/` directory), here are specific recommendations to make your requirements more robust and fully leverage the available data elements.

## 1. Data Governance & Integrity

The schema contains specific "control" columns that should be translated into strict business rules.

- **Territory Locking**: The `REP_PROFILE` table has `TERR1_LOCKED`, `TERR2_LOCKED`, etc.
  - **Requirement**: "The system must prevent automated territory reassignment for any Rep where the `TERR_LOCKED` flag is set to 'Y'."
  - **Requirement**: "An audit log must be generated whenever a locked territory is manually overridden."
- **Channel Management**: `CHANNEL_LOCKED` and `SUB_CHANNEL_LOCKED` exist.
  - **Requirement**: "Updates to Rep Channel/Sub-Channel from external feeds (e.g., 3rd party data) must be ignored if the Channel is locked."

## 2. Hierarchical Analysis

The data model supports deep hierarchical analysis that is currently underutilized.

- **Firm Hierarchy**: `FIRM` table has `MASTER_FIRM_ID` and `PARENT_FIRM_ID`.
  - **Requirement**: "Sales reporting must allow aggregation at three levels: Office, Firm, and Master Firm (Parent)."
  - **Requirement**: "Territory alignment must respect Master Firm relationships; if a Master Firm is assigned to a National Accounts manager, all child Firms should inherit this assignment."
- **Office Structure**: `OFFICE` table and `OFFICE_RELATIONSHIP` suggest a complex branch network.
  - **Requirement**: "The system must track sales roll-up through the Office hierarchy, handling cases where an Office reports to a different region than its physical location."

## 3. Salesforce Integration & Synchronization

Multiple tables (e.g., `TERRITORY_USER_SALESFORCE_LINK`, `OFFICE_SALESFORCE_LINK`) explicitly link SQL entities to Salesforce.

- **Bi-Directional Sync**:
  - **Requirement**: "The system must maintain a mapping table between SQL `CONTACT_ID` and Salesforce `ContactId`."
  - **Requirement**: "Changes to Territory assignments in SQL must trigger an update to the `UserTerritory` object in Salesforce via the API."
- **Orphan Management**:
  - **Requirement**: "A daily report must identify 'Orphaned' Reps who exist in Salesforce but have no corresponding record in the SQL `REP_PROFILE` table."

## 4. Product & Performance Analytics

The `TRANSACTION_HISTORY` table links to `FUND` and contains `TRANSACTION_TYPE`.

- **Net Flow Calculation**:
  - **Requirement**: "Net Flows must be calculated as `Sum(Purchases) - Sum(Redemptions)`."
  - **Requirement**: "The system must flag 'Large Ticket' redemptions (defined as > $100k) for immediate Wholesaler alert."
- **Product Mix**:
  - **Requirement**: "Advisor segmentation (Decile/Tier) must be calculated based on _Product-Specific_ sales goals, not just total gross sales."

## 5. Future Phase: "Golden Record"

The existence of `CONTACT_DUPLICATE` and `CONTACT_MATCHING_HASH` tables suggests a need for Master Data Management (MDM).

- **Deduplication**:
  - **Requirement**: "The system must implement a fuzzy matching algorithm (using Name + Zip + Firm) to identify potential duplicate Contacts across different source feeds."
