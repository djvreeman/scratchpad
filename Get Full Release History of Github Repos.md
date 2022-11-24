# Get Full Release History

### IG Publisher

Use Github CLI

```
gh auth login
gh api \
 -H "Accept: application/vnd.github+json" \
 /repos/HL7/fhir-ig-publisher/releases > SoftwareReleases/publisher-releases.json
```

Parse it with this python script

```
cd '/Users/dvreeman/odrive/Encryptor/B2/Documents/Work/HL7/Stats and Data Tracking'
python3 github-release-json-to-csv.py -i SoftwareReleases/publisher-releases.json -o SoftwareReleases/publisher-releases.csv
```



### FHIR Validator (org.hl7.fhir.core)

Use Github CLI

```
cd '/Users/dvreeman/odrive/Encryptor/B2/Documents/Work/HL7/Stats and Data Tracking'
gh auth login
gh api \
 -H "Accept: application/vnd.github+json" \
 /repos/hapifhir/org.hl7.fhir.core/releases > SoftwareReleases/org.hl7.fhir.core-releases.json
```

Parse it with this python script

```
python3 github-release-json-to-csv.py -i SoftwareReleases/org.hl7.fhir.core-releases.json -o SoftwareReleases/org.hl7.fhir.core-releases.csv
```



### FHIR Validator Wrapper (hapifhir/org.hl7.fhir.validator-wrapper)

User Github CLI

```
cd '/Users/dvreeman/odrive/Encryptor/B2/Documents/Work/HL7/Stats and Data Tracking'
gh auth login
gh api \
 -H "Accept: application/vnd.github+json" \
 /repos/hapifhir/org.hl7.fhir.validator-wrapper/releases > SoftwareReleases/org.hl7.fhir.validator-wrapper-releases.json
```

Parse it with this python script

```
python3 github-release-json-to-csv.py -i SoftwareReleases/org.hl7.fhir.validator-wrapper-releases.json -o SoftwareReleases/org.hl7.fhir.validator-wrapper-releases.csv
```

