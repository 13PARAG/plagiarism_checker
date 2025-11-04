


































# """
# CORRECTED Streamlit Frontend - Fixed UI and PDF Download
# File: frontend_app/app_enhanced.py - CORRECTED VERSION

# Fixes:
# 1. ✅ Yellow highlights (visible on dark background)
# 2. ✅ Actual PDF download (not HTML)
# 3. ✅ Better UI formatting
# """

# import streamlit as st
# import requests
# import os
# from datetime import datetime
# import json

# # ============ PAGE CONFIGURATION ============
# st.set_page_config(
#     page_title="Professional Plagiarism Checker",
#     page_icon="📄",
#     layout="wide",
#     initial_sidebar_state="expanded"
# )

# # ============ CUSTOM STYLING - IMPROVED ============
# st.markdown("""
# <style>
#     .main-header {
#         font-size: 3rem;
#         color: #1f77b4;
#         text-align: center;
#         margin-bottom: 1rem;
#         font-weight: bold;
#     }
    
#     /* FIXED: Yellow highlights with black text - VISIBLE on dark background */
#     mark {
#         background-color: #FFEB3B !important;
#         color: #000000 !important;
#         padding: 2px 4px;
#         border-radius: 3px;
#         font-weight: bold;
#     }
    
#     .highlight-section {
#         background-color: #f9f9f9;
#         padding: 15px;
#         border-radius: 10px;
#         border-left: 4px solid #1f77b4;
#         margin: 10px 0;
#         max-height: 400px;
#         overflow-y: auto;
#     }
    
#     .probability-bar {
#         background-color: #e0e0e0;
#         border-radius: 10px;
#         overflow: hidden;
#         height: 20px;
#         margin-top: 5px;
#     }
    
#     .probability-fill {
#         background: linear-gradient(90deg, #4caf50, #ffeb3b, #ff9800, #f44336);
#         height: 100%;
#         transition: width 0.3s ease;
#     }
    
#     .verdict-box {
#         padding: 20px;
#         border-radius: 10px;
#         text-align: center;
#         font-size: 24px;
#         font-weight: bold;
#     }
    
#     .plagiarized-high {
#         background-color: #FFEBEE;
#         color: #C62828;
#     }
    
#     .plagiarized-medium {
#         background-color: #FFF3E0;
#         color: #E65100;
#     }
    
#     .original {
#         background-color: #E8F5E9;
#         color: #2E7D32;
#     }
    
#     /* Improved download buttons */
#     .download-button {
#         padding: 12px 20px;
#         background-color: #1f77b4;
#         color: white;
#         border-radius: 5px;
#         text-align: center;
#         font-weight: bold;
#         margin: 5px;
#     }
# </style>
# """, unsafe_allow_html=True)

# # ============ CONFIGURATION ============
# API_URL = os.environ.get("API_URL", "http://localhost:5000")
# REQUEST_TIMEOUT = 120

# # ============ HELPER FUNCTIONS ============

# def check_api_status():
#     """Check if API is running"""
#     try:
#         response = requests.get(f"{API_URL}/", timeout=5)
#         if response.status_code == 200:
#             return response.json()
#     except:
#         pass
#     return None

# def check_google_config():
#     """Check if Google API is configured"""
#     try:
#         response = requests.get(f"{API_URL}/config_status", timeout=5)
#         if response.status_code == 200:
#             return response.json()
#     except:
#         pass
#     return None

# def download_pdf_report(results_data, mode):
#     """Download actual PDF report (not HTML)"""
#     try:
#         response = requests.post(
#             f"{API_URL}/generate_professional_pdf",
#             json={"data": results_data, "mode": mode},
#             timeout=30
#         )
        
#         if response.status_code == 200:
#             # Return actual PDF binary content
#             return response.content
#         else:
#             st.error(f"Error: {response.json().get('error')}")
#             return None
#     except Exception as e:
#         st.error(f"Error: {str(e)}")
#         return None

# # ============ SIDEBAR ============
# with st.sidebar:
#     st.markdown("## ⚙️ System Status")
#     st.markdown("---")
    
#     api_status = check_api_status()
#     if api_status:
#         st.success("✅ Backend API Connected")
#     else:
#         st.error("❌ Backend API Not Connected")
    
#     google_config = check_google_config()
#     if google_config and google_config.get('google_api_configured'):
#         st.success("✅ Google API Configured")
#     else:
#         st.warning("⚠️ Google API Not Configured")
    
#     st.markdown("---")
#     st.markdown("## 📋 Supported Formats")
#     st.markdown("""
#     **Upload Files:**
#     - 📄 TXT (Plain text)
#     - 📕 PDF (Documents)
#     - 📘 DOCX (Word files)
    
#     **Download Reports:**
#     - 📄 PDF (Professional)
#     - 📊 CSV (Data)
#     - 📋 JSON (Full info)
#     """)

# # ============ MAIN CONTENT ============
# st.markdown('<h1 class="main-header">📄 Professional Plagiarism Checker</h1>', unsafe_allow_html=True)
# st.markdown(
#     "<p style='text-align: center; color: #666; font-size: 1.1rem;'>"
#     "Advanced Detection • Multi-Format • Professional Reports</p>",
#     unsafe_allow_html=True
# )

# st.markdown("---")

# # Analysis mode selection
# col1, col2, col3 = st.columns([1, 2, 1])
# with col2:
#     analysis_type = st.radio(
#         "Choose Analysis Type:",
#         ["📋 Compare Local Documents", "🌐 Search Internet for Plagiarism"],
#         horizontal=True
#     )

# st.markdown("---")

# # Store results
# if 'results' not in st.session_state:
#     st.session_state.results = None
# if 'mode' not in st.session_state:
#     st.session_state.mode = None

# # ============ LOCAL COMPARISON MODE ============
# if "Compare" in analysis_type:
#     st.markdown("### 📋 Compare Two Documents")
    
#     # Custom threshold
#     threshold = st.slider(
#         "Set Plagiarism Threshold (%)",
#         min_value=30,
#         max_value=90,
#         value=50,
#         step=5
#     )
    
#     col1, col2 = st.columns(2)
    
#     with col1:
#         st.markdown("#### 📄 Original Document")
#         st.caption("Supported: TXT, PDF, DOCX")
#         original_file = st.file_uploader(
#             "Select original file",
#             type=["txt", "pdf", "docx"],
#             key="original"
#         )
#         if original_file:
#             st.success(f"✓ {original_file.name}")
    
#     with col2:
#         st.markdown("#### 📋 Submission Document")
#         st.caption("Supported: TXT, PDF, DOCX")
#         submission_file = st.file_uploader(
#             "Select submission file",
#             type=["txt", "pdf", "docx"],
#             key="submission"
#         )
#         if submission_file:
#             st.success(f"✓ {submission_file.name}")
    
#     st.markdown("---")
    
#     col1, col2, col3 = st.columns([1, 2, 1])
#     with col2:
#         if st.button("🔍 Compare Documents", type="primary", use_container_width=True):
#             if original_file and submission_file:
#                 with st.spinner("📊 Analyzing documents..."):
#                     try:
#                         files = {
#                             'original': original_file,
#                             'submission': submission_file
#                         }
                        
#                         response = requests.post(
#                             f"{API_URL}/check",
#                             files=files,
#                             timeout=REQUEST_TIMEOUT
#                         )
                        
#                         if response.status_code == 200:
#                             data = response.json()
#                             st.session_state.results = data
#                             st.session_state.mode = "local"
                            
#                             st.success("✅ Analysis Complete!")
#                             st.markdown("---")
                            
#                             # Metrics with progress bars
#                             col1, col2, col3 = st.columns(3)
                            
#                             with col1:
#                                 sim_pct = data['similarity_score'] * 100
#                                 st.metric("🔢 Similarity", f"{sim_pct:.2f}%")
#                                 st.markdown(f"""
#                                 <div class="probability-bar">
#                                     <div class="probability-fill" style="width: {min(sim_pct, 100)}%"></div>
#                                 </div>
#                                 """, unsafe_allow_html=True)
                            
#                             with col2:
#                                 prob_pct = data['probability'] * 100
#                                 st.metric("🤖 Probability", f"{prob_pct:.2f}%")
#                                 st.markdown(f"""
#                                 <div class="probability-bar">
#                                     <div class="probability-fill" style="width: {min(prob_pct, 100)}%"></div>
#                                 </div>
#                                 """, unsafe_allow_html=True)
                            
#                             with col3:
#                                 is_plagiarized = sim_pct >= threshold
#                                 if is_plagiarized:
#                                     if sim_pct >= 75:
#                                         st.markdown('<div class="verdict-box plagiarized-high">🔴 PLAGIARIZED</div>', unsafe_allow_html=True)
#                                     else:
#                                         st.markdown('<div class="verdict-box plagiarized-medium">🟠 SUSPICIOUS</div>', unsafe_allow_html=True)
#                                 else:
#                                     st.markdown('<div class="verdict-box original">🟢 ORIGINAL</div>', unsafe_allow_html=True)
                            
#                             # Text comparison - FIXED: Better highlight visibility
#                             st.markdown("---")
#                             st.subheader("🔍 Text Comparison with Highlights (Yellow = Matching Text)")
                            
#                             col1, col2 = st.columns(2)
#                             with col1:
#                                 st.markdown("**Original Document:**")
#                                 with st.container():
#                                     st.markdown(
#                                         f"""<div class="highlight-section">{data['highlighted_original']}</div>""",
#                                         unsafe_allow_html=True
#                                     )
                            
#                             with col2:
#                                 st.markdown("**Submission Document:**")
#                                 with st.container():
#                                     st.markdown(
#                                         f"""<div class="highlight-section">{data['highlighted_submission']}</div>""",
#                                         unsafe_allow_html=True
#                                     )
                        
#                         else:
#                             st.error(f"❌ Error: {response.json().get('error')}")
                    
#                     except Exception as e:
#                         st.error(f"❌ Error: {str(e)}")
#             else:
#                 st.warning("⚠️ Upload both documents")

# # ============ INTERNET SEARCH MODE ============
# else:
#     st.markdown("### 🌐 Search Internet for Plagiarism")
    
#     google_config = check_google_config()
#     if not google_config or not google_config.get('google_api_configured'):
#         st.error("❌ Google API Not Configured")
#     else:
#         st.success("✅ Google API Ready")
        
#         submission_file = st.file_uploader(
#             "Upload document",
#             type=["txt", "pdf", "docx"],
#             key="internet_submission"
#         )
        
#         if submission_file:
#             st.success(f"✓ {submission_file.name}")
        
#         col1, col2, col3 = st.columns([1, 2, 1])
#         with col2:
#             if st.button("🌐 Search Internet", type="primary", use_container_width=True):
#                 if submission_file:
#                     with st.spinner("🔍 Searching internet... (30-60 seconds)"):
#                         try:
#                             files = {'submission': submission_file}
                            
#                             response = requests.post(
#                                 f"{API_URL}/check_internet",
#                                 files=files,
#                                 timeout=120
#                             )
                            
#                             if response.status_code == 200:
#                                 data = response.json()
#                                 st.session_state.results = data
#                                 st.session_state.mode = "internet"
                                
#                                 st.success("✅ Search Complete!")
#                                 st.markdown("---")
                                
#                                 col1, col2, col3 = st.columns(3)
#                                 with col1:
#                                     st.metric("🔎 Matches", data['total_matches_found'])
                                
#                                 with col2:
#                                     st.metric("📊 Highest Similarity", f"{data.get('highest_similarity', 0) * 100:.2f}%")
                                
#                                 with col3:
#                                     verdict = data.get('overall_verdict', 'UNKNOWN')
#                                     st.markdown(f"<h3 style='color: {'red' if 'PLAGIARIZED' in verdict else 'green'}; text-align: center;'>{verdict}</h3>", unsafe_allow_html=True)
                                
#                                 st.markdown("---")
#                                 st.subheader("🎯 Top Matches from Internet")
                                
#                                 for idx, match in enumerate(data.get('internet_matches', []), 1):
#                                     with st.expander(f"Match #{idx} - {match['title'][:60]}... ({match['similarity_score']*100:.1f}%)", expanded=(idx==1)):
#                                         col1, col2 = st.columns([1, 2])
                                        
#                                         with col1:
#                                             st.metric("Similarity", f"{match['similarity_score']*100:.2f}%")
#                                             st.metric("Probability", f"{match['probability']*100:.2f}%")
                                            
#                                             if match['plagiarized']:
#                                                 st.error("🔴 Plagiarized")
#                                             else:
#                                                 st.success("🟢 Original")
                                        
#                                         with col2:
#                                             st.markdown(f"**Title:** {match['title']}")
#                                             st.markdown(f"**URL:** [{match['url']}]({match['url']})")
#                                             st.markdown(f"**Snippet:** {match['snippet'][:300]}...")
                            
#                             else:
#                                 st.error(f"❌ Error: {response.json().get('error')}")
                        
#                         except Exception as e:
#                             st.error(f"❌ Error: {str(e)}")
#                 else:
#                     st.warning("⚠️ Upload a document")

# # ============ DOWNLOAD SECTION - FIXED: ACTUAL PDF DOWNLOAD ============
# if st.session_state.results:
#     st.markdown("---")
#     st.markdown("### 📥 Download Reports")
    
#     col1, col2, col3, col4 = st.columns(4)
    
#     # FIXED: Actual PDF Download
#     with col1:
#         if st.button("📄 PDF Report", use_container_width=True, help="Professional PDF with highlights"):
#             with st.spinner("Generating PDF..."):
#                 pdf_content = download_pdf_report(st.session_state.results, st.session_state.mode)
#                 if pdf_content:
#                     st.download_button(
#                         label="⬇️ Download PDF",
#                         data=pdf_content,
#                         file_name=f"plagiarism_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
#                         mime="application/pdf",
#                         use_container_width=True
#                     )
    
#     # CSV Export
#     with col2:
#         if st.session_state.mode == "local":
#             csv_data = f"Similarity,Probability,Verdict,Timestamp\n{st.session_state.results.get('similarity_score', 0) * 100:.2f}%,{st.session_state.results.get('probability', 0) * 100:.2f}%,{'PLAGIARIZED' if st.session_state.results.get('plagiarized') else 'ORIGINAL'},{datetime.now()}"
#         else:
#             csv_data = "Match,Title,URL,Similarity,Status\n"
#             for idx, m in enumerate(st.session_state.results.get('internet_matches', []), 1):
#                 csv_data += f"{idx},{m.get('title', 'N/A')},{m.get('url', 'N/A')},{m.get('similarity_score', 0) * 100:.2f}%,{'PLAGIARIZED' if m.get('plagiarized') else 'ORIGINAL'}\n"
        
#         st.download_button(
#             label="📊 Download CSV",
#             data=csv_data,
#             file_name=f"data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
#             mime="text/csv",
#             use_container_width=True
#         )
    
#     # JSON Export
#     with col3:
#         st.download_button(
#             label="📋 Download JSON",
#             data=json.dumps(st.session_state.results, indent=2),
#             file_name=f"results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
#             mime="application/json",
#             use_container_width=True
#         )
    
#     # Snippets
#     with col4:
#         if st.session_state.mode == "internet":
#             snippets = "\n\n".join([
#                 f"Match {i+1}: {m['title']}\nURL: {m['url']}\n{m['snippet']}\n"
#                 for i, m in enumerate(st.session_state.results.get('internet_matches', []))
#             ])
#             st.download_button(
#                 label="📝 Snippets",
#                 data=snippets,
#                 file_name=f"snippets_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
#                 mime="text/plain",
#                 use_container_width=True
#             )

# # ============ FOOTER ============
# st.markdown("---")
# st.markdown("""
# <div style='text-align: center; color: #999; font-size: 0.9rem;'>
#     <p><b>Advanced Plagiarism Checker v3.0 - Final Edition</b></p>
#     <p>✅ Multi-Format | ✅ Professional Reports | ✅ Visible Highlighting | ✅ PDF Download</p>
# </div>
# """, unsafe_allow_html=True)













































"""
FINAL CORRECTED Streamlit Frontend
File: frontend_app/app_enhanced.py
"""

import streamlit as st
import requests
import os
from datetime import datetime
import json

# PAGE CONFIGURATION
st.set_page_config(
    page_title="Professional Plagiarism Checker",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CUSTOM STYLING - FULLY FIXED
st.markdown("""
<style>
.main-header {
    font-size: 3rem;
    color: #1f77b4;
    text-align: center;
    margin-bottom: 1rem;
    font-weight: bold;
}

/* FIXED: Dark background with white text for ALL content */
.highlight-section {
    background-color: #ffffff !important;  /* white background */
    color: #000000 !important;             /* black text */
    padding: 15px !important;
    border-radius: 10px !important;
    border-left: 4px solid #1f77b4 !important;
    margin: 10px 0 !important;
    max-height: 400px !important;
    overflow-y: auto !important;
    font-family: 'Courier New', monospace !important;
    line-height: 1.6 !important;
}

/* Ensure ALL nested elements have white text */
.highlight-section * {
    color: #000000 !important;
}

/* Yellow highlights - BRIGHT and VISIBLE */
mark {
    background-color: #FFEB3B !important;
    color: #000000 !important;
    padding: 2px 4px !important;
    border-radius: 3px !important;
    font-weight: bold !important;
}

.probability-bar {
    background-color: #e0e0e0;
    border-radius: 10px;
    overflow: hidden;
    height: 20px;
    margin-top: 5px;
}

.probability-fill {
    background: linear-gradient(90deg, #4caf50, #ffeb3b, #ff9800, #f44336);
    height: 100%;
    transition: width 0.3s ease;
}

.verdict-box {
    padding: 20px;
    border-radius: 10px;
    text-align: center;
    font-size: 24px;
    font-weight: bold;
}

.plagiarized-high {
    background-color: #FFEBEE;
    color: #C62828;
}

.plagiarized-medium {
    background-color: #FFF3E0;
    color: #E65100;
}

.original {
    background-color: #E8F5E9;
    color: #2E7D32;
}
</style>
""", unsafe_allow_html=True)

# CONFIGURATION
API_URL = os.environ.get("API_URL", "APIURL=https://plagiarism-checker-ukpr.onrender.com")
REQUEST_TIMEOUT = 120

# HELPER FUNCTIONS
def check_api_status():
    try:
        response = requests.get(f"{API_URL}/", timeout=5)
        if response.status_code == 200:
            return response.json()
    except:
        pass
    return None

def check_google_config():
    try:
        response = requests.get(f"{API_URL}/config_status", timeout=5)
        if response.status_code == 200:
            return response.json()
    except:
        pass
    return None

def download_pdf_report(results_data, mode):
    try:
        response = requests.post(
            f"{API_URL}/generate_professional_pdf",
            json={"data": results_data, "mode": mode},
            timeout=30
        )
        if response.status_code == 200:
            return response.content
        else:
            st.error(f"Error: {response.json().get('error')}")
            return None
    except Exception as e:
        st.error(f"Error: {str(e)}")
        return None

# SIDEBAR
with st.sidebar:
    st.markdown("## ⚙️ System Status")
    st.markdown("---")
    
    api_status = check_api_status()
    if api_status:
        st.success("✅ Backend API Connected")
    else:
        st.error("❌ Backend API Not Connected")
    
    google_config = check_google_config()
    if google_config and google_config.get('google_api_configured'):
        st.success("✅ Google API Configured")
    else:
        st.warning("⚠️ Google API Not Configured")
    
    st.markdown("---")
    st.markdown("## 📋 Supported Formats")
    st.markdown("""
    **Upload Files:**
    - 📄 TXT (Plain text)
    - 📕 PDF (Documents)
    - 📘 DOCX (Word files)
    
    **Download Reports:**
    - 📄 PDF (Professional)
    - 📊 CSV (Data)
    - 📋 JSON (Full info)
    """)

# MAIN CONTENT
st.markdown('<h1 class="main-header">📄 Professional Plagiarism Checker</h1>', unsafe_allow_html=True)
st.markdown(
    "<p style='text-align: center; color: #666; font-size: 1.1rem;'>"
    "Advanced Detection • Multi-Format • Professional Reports</p>",
    unsafe_allow_html=True
)

st.markdown("---")

# Analysis mode selection
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    analysis_type = st.radio(
        "Choose Analysis Type:",
        ["📋 Compare Local Documents", "🌐 Search Internet for Plagiarism"],
        horizontal=True
    )

st.markdown("---")

# Store results
if 'results' not in st.session_state:
    st.session_state.results = None
if 'mode' not in st.session_state:
    st.session_state.mode = None

# LOCAL COMPARISON MODE
if "Compare" in analysis_type:
    st.markdown("### 📋 Compare Two Documents")
    
    threshold = st.slider(
        "Set Plagiarism Threshold (%)",
        min_value=30,
        max_value=90,
        value=50,
        step=5
    )
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 📄 Original Document")
        st.caption("Supported: TXT, PDF, DOCX")
        original_file = st.file_uploader(
            "Select original file",
            type=["txt", "pdf", "docx"],
            key="original"
        )
        if original_file:
            st.success(f"✓ {original_file.name}")
    
    with col2:
        st.markdown("#### 📋 Submission Document")
        st.caption("Supported: TXT, PDF, DOCX")
        submission_file = st.file_uploader(
            "Select submission file",
            type=["txt", "pdf", "docx"],
            key="submission"
        )
        if submission_file:
            st.success(f"✓ {submission_file.name}")
    
    st.markdown("---")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🔍 Compare Documents", type="primary", use_container_width=True):
            if original_file and submission_file:
                with st.spinner("📊 Analyzing documents..."):
                    try:
                        files = {
                            'original': original_file,
                            'submission': submission_file
                        }
                        
                        response = requests.post(
                            f"{API_URL}/check",
                            files=files,
                            timeout=REQUEST_TIMEOUT
                        )
                        
                        if response.status_code == 200:
                            data = response.json()
                            st.session_state.results = data
                            st.session_state.mode = "local"
                            
                            st.success("✅ Analysis Complete!")
                            st.markdown("---")
                            
                            # Metrics
                            col1, col2, col3 = st.columns(3)
                            
                            with col1:
                                sim_pct = data['similarity_score'] * 100
                                st.metric("🔢 Similarity", f"{sim_pct:.2f}%")
                                st.markdown(f"""
                                <div class="probability-bar">
                                    <div class="probability-fill" style="width: {min(sim_pct, 100)}%"></div>
                                </div>
                                """, unsafe_allow_html=True)
                            
                            with col2:
                                prob_pct = data['probability'] * 100
                                st.metric("🤖 Probability", f"{prob_pct:.2f}%")
                                st.markdown(f"""
                                <div class="probability-bar">
                                    <div class="probability-fill" style="width: {min(prob_pct, 100)}%"></div>
                                </div>
                                """, unsafe_allow_html=True)
                            
                            with col3:
                                is_plagiarized = sim_pct >= threshold
                                if is_plagiarized:
                                    if sim_pct >= 75:
                                        st.markdown('<div class="verdict-box plagiarized-high">🔴 PLAGIARIZED</div>', unsafe_allow_html=True)
                                    else:
                                        st.markdown('<div class="verdict-box plagiarized-medium">🟠 SUSPICIOUS</div>', unsafe_allow_html=True)
                                else:
                                    st.markdown('<div class="verdict-box original">🟢 ORIGINAL</div>', unsafe_allow_html=True)
                            
                            # Text comparison - FIXED
                            st.markdown("---")
                            st.subheader("🔍 Text Comparison with Highlights (Yellow = Matching Text)")
                            
                            col1, col2 = st.columns(2)
                            with col1:
                                st.markdown("**📄 Original Document:**")
                                st.markdown(
                                    f'<div class="highlight-section">{data["highlighted_original"]}</div>',
                                    unsafe_allow_html=True
                                )
                            
                            with col2:
                                st.markdown("**📋 Submission Document:**")
                                st.markdown(
                                    f'<div class="highlight-section">{data["highlighted_submission"]}</div>',
                                    unsafe_allow_html=True
                                )
                        
                        else:
                            st.error(f"❌ Error: {response.json().get('error')}")
                    
                    except Exception as e:
                        st.error(f"❌ Error: {str(e)}")
            else:
                st.warning("⚠️ Upload both documents")

# INTERNET SEARCH MODE
else:
    st.markdown("### 🌐 Search Internet for Plagiarism")
    
    google_config = check_google_config()
    if not google_config or not google_config.get('google_api_configured'):
        st.error("❌ Google API Not Configured")
    else:
        st.success("✅ Google API Ready")
        
        submission_file = st.file_uploader(
            "Upload document",
            type=["txt", "pdf", "docx"],
            key="internet_submission"
        )
        
        if submission_file:
            st.success(f"✓ {submission_file.name}")
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("🌐 Search Internet", type="primary", use_container_width=True):
                if submission_file:
                    with st.spinner("🔍 Searching internet... (30-60 seconds)"):
                        try:
                            files = {'submission': submission_file}
                            
                            response = requests.post(
                                f"{API_URL}/check_internet",
                                files=files,
                                timeout=120
                            )
                            
                            if response.status_code == 200:
                                data = response.json()
                                st.session_state.results = data
                                st.session_state.mode = "internet"
                                
                                st.success("✅ Search Complete!")
                                st.markdown("---")
                                
                                col1, col2, col3 = st.columns(3)
                                with col1:
                                    st.metric("🔎 Matches", data['total_matches_found'])
                                
                                with col2:
                                    st.metric("📊 Highest Similarity", f"{data.get('highest_similarity', 0) * 100:.2f}%")
                                
                                with col3:
                                    verdict = data.get('overall_verdict', 'UNKNOWN')
                                    st.markdown(f"<h3 style='color: {'red' if 'PLAGIARIZED' in verdict else 'green'}; text-align: center;'>{verdict}</h3>", unsafe_allow_html=True)
                                
                                st.markdown("---")
                                st.subheader("🎯 Top Matches from Internet")
                                
                                for idx, match in enumerate(data.get('internet_matches', []), 1):
                                    with st.expander(f"Match #{idx} - {match['title'][:60]}... ({match['similarity_score']*100:.1f}%)", expanded=(idx==1)):
                                        col1, col2 = st.columns([1, 2])
                                        
                                        with col1:
                                            st.metric("Similarity", f"{match['similarity_score']*100:.2f}%")
                                            st.metric("Probability", f"{match['probability']*100:.2f}%")
                                            
                                            if match['plagiarized']:
                                                st.error("🔴 Plagiarized")
                                            else:
                                                st.success("🟢 Original")
                                        
                                        with col2:
                                            st.markdown(f"**Title:** {match['title']}")
                                            st.markdown(f"**URL:** [{match['url']}]({match['url']})")
                                            st.markdown(f"**Snippet:** {match['snippet'][:300]}...")
                            
                            else:
                                st.error(f"❌ Error: {response.json().get('error')}")
                        
                        except Exception as e:
                            st.error(f"❌ Error: {str(e)}")
                else:
                    st.warning("⚠️ Upload a document")

# DOWNLOAD SECTION
if st.session_state.results:
    st.markdown("---")
    st.markdown("### 📥 Download Reports")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("📄 PDF Report", use_container_width=True):
            with st.spinner("Generating PDF..."):
                pdf_content = download_pdf_report(st.session_state.results, st.session_state.mode)
                if pdf_content:
                    st.download_button(
                        label="⬇️ Download PDF",
                        data=pdf_content,
                        file_name=f"plagiarism_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
                        mime="application/pdf",
                        use_container_width=True
                    )
    
    with col2:
        if st.session_state.mode == "local":
            csv_data = f"Similarity,Probability,Verdict,Timestamp\n{st.session_state.results.get('similarity_score', 0) * 100:.2f}%,{st.session_state.results.get('probability', 0) * 100:.2f}%,{'PLAGIARIZED' if st.session_state.results.get('plagiarized') else 'ORIGINAL'},{datetime.now()}"
        else:
            csv_data = "Match,Title,URL,Similarity,Status\n"
            for idx, m in enumerate(st.session_state.results.get('internet_matches', []), 1):
                csv_data += f"{idx},{m.get('title', 'N/A')},{m.get('url', 'N/A')},{m.get('similarity_score', 0) * 100:.2f}%,{'PLAGIARIZED' if m.get('plagiarized') else 'ORIGINAL'}\n"
        
        st.download_button(
            label="📊 Download CSV",
            data=csv_data,
            file_name=f"data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv",
            use_container_width=True
        )
    
    with col3:
        st.download_button(
            label="📋 Download JSON",
            data=json.dumps(st.session_state.results, indent=2),
            file_name=f"results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
            mime="application/json",
            use_container_width=True
        )
    
    with col4:
        if st.session_state.mode == "internet":
            snippets = "\n\n".join([
                f"Match {i+1}: {m['title']}\nURL: {m['url']}\n{m['snippet']}\n"
                for i, m in enumerate(st.session_state.results.get('internet_matches', []))
            ])
            st.download_button(
                label="📝 Snippets",
                data=snippets,
                file_name=f"snippets_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                mime="text/plain",
                use_container_width=True
            )

# FOOTER
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #999; font-size: 0.9rem;'>
    <p><b>Advanced Plagiarism Checker v3.0 - Final Edition</b></p>
    <p>✅ Multi-Format | ✅ Professional Reports | ✅ Visible Highlighting | ✅ PDF Download</p>
</div>
""", unsafe_allow_html=True)
