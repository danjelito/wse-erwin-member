# Erwin Member Processor

This is a program to clean the member data from Erwin.

## Data Source:

**Erwin Member Data**

- Extracted from Erwin - memberships.
- Filter:
  - from between 2015-2028
  - active true or false
- Export template "Devan - Repurchase Rate and Member Pop"

## How to Use:

1. Export the data from Erwin - Memberships with export template `Repurcahase Rate & Member Pop`.
2. Put the file inside `input` folder, change the filename to exported date.
3. Make sure all membership codes are mapped in `input/membership_mapping.xlsx`
4. Process & clean the data using `main.ipynb`
5. The output will be stored inside `output` folder in parquet format.
6. Use separate notebook for separate use cases:
   - `modules/other_membership_pop.ipynb`: to find the number of additional membership members per month.
   - `modules/club_member_demo.ipynb`: to find the demographic of club members (ad-hoc, requested by Diana).
   - `modules/repurchase_rate.ipynb`: to find the repurchase rate per month (ad-hoc, requested by Chandra).
   - `modules/cpt_member_pop.ipynb`: to find the number of cpt members per month. **somehow the number is too low compared to what intan provides**.

## Usage:

The output of this program is used for:

1. Raw data for Experience Management Report - Member Activity Diagram (there are other membership population there).
2. [Member Population Report](https://docs.google.com/spreadsheets/d/1oIq_27yHAZ8WB5F3cKg-tfoBpT7woDqh/edit#gid=1001742099).
3. Member Population per Center Report (in Experience Management Report).

## Todo:

1. Create secret env.
