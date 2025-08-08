<pre>
📁 autogen_som_hitl/
├── 📄 .env
├── 📄 config.py
├── 📄 main.py
├── 📄 requirements.txt
├── 📁 agents/
│   ├── 📄 __init__.py
│   ├── 📄 inner_team.py
│   └── 📄 outer_team.py
├── 📁 flows/
│   ├── 📄 __init__.py
│   ├── 📄 inner_flow.py
│   └── 📄 outer_flow.py
├── 📁 tools/                    ← **NEW: Create this directory**
│   ├── 📄 __init__.py
│   ├── 📄 dispatcher.py         ← **DynamicToolDispatcher goes here**
│   ├── 📄 environmental_tools.py
│   ├── 📄 web_search_tools.py
│   └── 📄 analysis_tools.py
└── 📁 utils/                    ← **Optional: For utility functions**
    ├── 📄 __init__.py
    └── 📄 patterns.py
</pre>
