# SOURCES.md

## SAP Source

### Real-world format researched

Enterprise ERP ESG exports from SAP sustainability and emissions modules.

### Sample data used

* emission_type
* unit
* quantity
* facility
* timestamp

### What would break in production

* inconsistent units
* missing timestamps
* duplicate exports
* malformed CSV rows

---

## Utility Source

### Real-world format researched

Electricity and utility consumption statements.

### Sample data used

* kWh usage
* billing period
* region
* supplier

### What would break in production

* OCR extraction issues
* varying utility provider formats
* timezone inconsistencies

---

## Travel Source

### Real-world format researched

Corporate travel and transportation emissions exports.

### Sample data used

* travel mode
* distance
* employee identifier
* trip date

### What would break in production

* duplicate itineraries
* incomplete route data
* unsupported transport formats
