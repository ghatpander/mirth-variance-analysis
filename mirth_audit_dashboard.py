import streamlit as st
import streamlit.components.v1 as components
from bs4 import BeautifulSoup

# Updated clean structure-only baseline
BASELINE_JSON = """
{
  "Messages": {
    "MSH": {
      "SegmentId": "", "EncodingCharacters": "", "SendingApplication": "", "SendingFacility": "", 
      "ReceivingApplication": "", "ReceivingFacility": "", "DateTimeOfMessage": "", "Security": "", 
      "MessageType": "", "MessageControlId": "", "ProcessingId": "", "VersionId": "", 
      "SequenceNumber": "", "ContinuationPointer": "", "AcceptAcknowledgementType": "", 
      "ApplicationAcknowledgementType": "", "CountryCode": ""
    },
    "EVN": {
      "SegmentId": "", "EventTypeCode": "", "DateTimeOfEvent": "", "DateTimeOfPlannedEvent": "", 
      "EventReasonCode": "", "OperatorID": "", "EventOccured": ""
    },
    "PID": {
      "SegmentId": "", "PatientExternalId": "", "PatientInternalId": "", "AlternatePatientId": "", 
      "Title": "", "FirstName": "", "MiddleName": "", "LastName": "", "MotherMaidenName": "", 
      "DateOfBirth": "", "Sex": "", "PatientAlias": "", "Race": "", "PatientAddress": "", 
      "CountyCode": "", "HomePhoneNumber": "", "BusinessPhoneNumber": "", "PrimaryLanguage": "", 
      "MaritalStatus": "", "Religion": "", "PatientAccountNumber": "", "SSN": "", 
      "DriverLicenseNumber": "", "MotherIdentifier": "", "EthnicGroup": "", "BirthPlace": "", 
      "MultipleBirthIndicator": "", "BirthOrder": "", "Citizenship": "", "VeteransMilitaryStatus": "", 
      "Nationality": "", "PatientDeathDateAndTime": "", "PatientDeathIndicator": ""
    },
    "PV1": {
      "SegmentId": "", "PatientClass": "", "Unit": "", "Floor": "", "Room": "", "Bed": "", 
      "AdmissionType": "", "PreAdmitNumber": "", "PriorLocationNumber": "", "AttendingDoctor": "", 
      "ReferringDoctor": "", "ConsultingDoctor": "", "HospitalService": "", "TemporaryLocation": "", 
      "PreAdmitTestIndicator": "", "ReadmissionIndicator": "", "AdmitSource": "", 
      "AmbulatoryStatus": "", "VIPIndicator": "", "AdmittingDoctor": "", "PatientType": "", 
      "VisitNumber": "", "FinancialClass": "", "ChargePriceIndicator": "", "CourtesyCode": "", 
      "CreditRating": "", "ContactCode": "", "ContractEffectiveDate": "", "ContractAmount": "", 
      "ContractPeriod": "", "InterestCode": "", "TransferToBadDebtCode": "", "TransferToBadDebtDate": "", 
      "BadDebtAgencyCode": "", "BadDebtTransferCode": "", "BadDebtRecoveryAmount": "", 
      "DeleteAccountIndicator": "", "DeleteAccountDate": "", "DischargeDisposition": "", 
      "DischargedToLocation": "", "DietType": "", "ServicingFacility": "", "BedStatus": "", 
      "AccountStatus": "", "PendingLocation": "", "PriorTemporaryLocation": "", "AdmitDateTime": ""
    },
    "IAM": {
      "Id": "", "Name": "", "Type": "", "Action": "", "SourceSegment": ""
    },
    "ODS": {
      "SegmentId": "", "ServicePeriod": "", "DietSupplementOrPreferenceCode": "", "Diet" : "", 
      "Texture" : "", "Fluid" : "", "Modifiers": [], "NPOFlag": "", "DietaryNotes": "", "Action": ""
    },
    "NTE": {
      "Source": "", "Comment": ""
    }
  }
}
"""

def get_all_steps(xml_content):
    soup = BeautifulSoup(xml_content, 'xml')
    steps = {}
    for step in soup.find_all(lambda tag: tag.name and 'JavaScriptStep' in tag.name):
        name = step.find('name')
        if name:
            steps[name.text] = step.find('script').text or ""
    return steps

st.set_page_config(layout="wide")
st.title("Integration Variance Analysis")

uploaded_files = st.file_uploader("Upload All XMLs", accept_multiple_files=True, type=['xml'])

if uploaded_files:
    if 'data' not in st.session_state:
        st.session_state.data = {f.name: get_all_steps(f.read().decode('utf-8')) for f in uploaded_files}
    
    data = st.session_state.data
    all_steps = sorted(set().union(*[c.keys() for c in data.values()]))

    st.markdown("""
        <style>
        .code-container { height: 300px; overflow: scroll; border: 1px solid #ccc; padding: 10px; background: #f0f0f0; font-family: monospace; }
        </style>
    """, unsafe_allow_html=True)

    for step in all_steps:
        with st.expander(f"Analysis: {step}", expanded=False):
            # Dynamic columns based on number of uploaded files
            files = list(data.keys())
            cols = st.columns(len(files))
            for i, fname in enumerate(files):
                with cols[i]:
                    st.markdown(f"**{fname}**")
                    st.markdown(f'<div class="code-container"><pre>{data[fname].get(step, "MISSING")}</pre></div>', unsafe_allow_html=True)
            
            if st.button(f"Run Variance Analysis: {step}", key=f"btn_{step}"):
                # Build the prompt dynamically to include ALL blocks and the baseline
                scripts_data = "\n\n".join([f"--- SCRIPT: {f} ---\n{data[f].get(step, '')}" for f in files])
                
                prompt = f"""
                You are a technical auditor. Compare the following Mirth scripts for step '{step}' against each other and the provided baseline JSON schema.
                
                BASELINE SCHEMA:
                {BASELINE_JSON}
                
                SCRIPTS TO ANALYZE:
                {scripts_data}
                
                TASK:
                1. Variance Analysis: Contrast how each script implements the logic (data extraction, parsing, and type handling) vs. the others.
                2. Baseline Fidelity: Compare each script's output structure vs. the BASELINE SCHEMA provided.
                3. Complexity Ranking: Rank the scripts by logical complexity and explain why (e.g., nesting, conditionals, error handling).
                
                STRICT RULES:
                - Do NOT provide recommendations or suggestions.
                - Be concise, technical, and precise.
                - Use the file names provided.
                """
                
                components_html = f"""
                <script src="https://js.puter.com/v2/"></script>
                <div id="output" style="white-space: pre-wrap; font-family: sans-serif; height: 500px; overflow: scroll; border: 1px solid #ddd; padding: 10px; background: #fff;">Running variance analysis...</div>
                <script>
                    async function run() {{
                        const res = await puter.ai.chat(`{prompt}`);
                        document.getElementById('output').innerText = res;
                    }}
                    run();
                </script>
                """
                components.html(components_html, height=550)