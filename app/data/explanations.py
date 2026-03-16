# Dimension explanation cards — shown when user clicks a risk tag in the result breakdown.
# Each dimension (Q1-Q8) has explanations for each risk tier, grounded in research.
#
# Research basis:
# [A] Anthropic "Observed Exposure" (2026) — actual API usage patterns
# [S] Stanford "Canary in the Coal Mine" (Brynjolfsson et al., 2025) — codified vs tacit knowledge
# [H] HBS & BCG "Jagged Technological Frontier" (2023) — inside vs outside the frontier

# Keys: dimension index (0-7) → score range → explanation
# Q1 scores are 1-7, Q2-Q8 scores are 1-4

DIMENSION_EXPLANATIONS = {
    # ── Q1: 职业类型 ──
    0: {
        "title_zh": "职业类型",
        "title_en": "Job Type",
        "tiers": {
            "high": {  # score >= 5
                "zh": (
                    "根据 Anthropic 的观测暴露度研究，您所在的职业类型的核心任务正在被 AI 以 API 调用的方式全自动处理。"
                    "斯坦福的研究指出，这类工作的知识基础高度显性化（Codified），即任务规则可以被明确写出并交给机器执行。"
                    "哈佛/BCG 的研究将这类任务归类为「技术前沿内」，AI 不仅能完成，而且质量和速度往往优于人类。"
                ),
                "en": (
                    "According to Anthropic's Observed Exposure study, the core tasks in your occupation are already being fully automated via AI API calls. "
                    "Stanford's research shows this type of work relies heavily on Codified Knowledge — rules that can be explicitly written down and handed to machines. "
                    "The HBS/BCG study classifies these tasks as 'inside the frontier,' where AI matches or exceeds human performance."
                ),
            },
            "medium": {  # score 3-4
                "zh": (
                    "Anthropic 的研究显示，您所在职业的部分任务已出现 AI 自动化的迹象，但尚未全面覆盖。"
                    "斯坦福的研究认为，这类工作混合了显性知识和隐性知识 —— AI 能处理规则化的部分，但经验判断仍需人类把关。"
                    "哈佛/BCG 的研究警告：在这类混合领域，盲目信任 AI 产出的人反而表现更差（下降 19%），关键在于学会审核而非依赖。"
                ),
                "en": (
                    "Anthropic's research shows some tasks in your occupation are being automated, but coverage is incomplete. "
                    "Stanford's framework places this work at the boundary of Codified and Tacit Knowledge — AI handles the rule-based parts, but experience-based judgment remains human. "
                    "The HBS/BCG study warns: in these mixed domains, workers who blindly trust AI output actually perform 19% worse. The key is learning to review, not rely."
                ),
            },
            "low": {  # score <= 2
                "zh": (
                    "Anthropic 的 API 使用日志分析显示，您所在职业的核心任务几乎没有出现在 AI 自动化调用中。"
                    "斯坦福的研究将这类工作归类为高度依赖隐性知识（Tacit Knowledge）—— 多年积累的直觉、人际判断和物理技能，难以编码为机器指令。"
                    "哈佛/BCG 的研究确认，这类任务处于「技术前沿之外」，AI 目前无法有效介入。"
                ),
                "en": (
                    "Anthropic's API usage analysis shows the core tasks in your occupation barely appear in AI automation logs. "
                    "Stanford classifies this work as heavily reliant on Tacit Knowledge — years of intuition, interpersonal judgment, and physical skills that can't be encoded into machine instructions. "
                    "The HBS/BCG study confirms these tasks are 'outside the frontier' — AI cannot effectively intervene."
                ),
            },
        },
    },

    # ── Q2: 数字化暴露 ──
    1: {
        "title_zh": "数字化暴露",
        "title_en": "Digital Exposure",
        "tiers": {
            "high": {
                "zh": (
                    "您几乎全天在电脑前工作。Anthropic 的研究表明，高度数字化的工作流程是 AI 渗透的首要条件——"
                    "当您的全部输入和输出都在数字系统中流转时，AI 可以无缝接入每一个环节。"
                    "斯坦福的研究发现，数字化程度最高的职业（软件开发、数据分析）正是 AI 替代效应最强的领域。"
                ),
                "en": (
                    "You spend nearly all day at a computer. Anthropic's research shows high digital workflow is the primary condition for AI penetration — "
                    "when all your inputs and outputs flow through digital systems, AI can seamlessly plug into every step. "
                    "Stanford found that the most digitized occupations (software development, data analysis) show the strongest AI displacement effects."
                ),
            },
            "medium": {
                "zh": (
                    "您的工作混合了数字和线下环节。哈佛/BCG 的研究表明，这种混合模式提供了天然的缓冲——"
                    "AI 可以接管数字化部分，但线下沟通和非数字任务构成了 AI 无法逾越的「物理断层」。"
                    "关键在于：您在数字部分的效率可以被 AI 大幅提升，但线下部分的价值反而会因此凸显。"
                ),
                "en": (
                    "Your work mixes digital and offline components. HBS/BCG research shows this hybrid mode provides a natural buffer — "
                    "AI can take over the digital parts, but offline communication and non-digital tasks create a 'physical gap' AI cannot cross. "
                    "Key insight: AI can dramatically boost your digital efficiency, but your offline value becomes even more prominent as a result."
                ),
            },
            "low": {
                "zh": (
                    "您的工作几乎不依赖电脑。Anthropic 的 API 使用数据中，完全离线的职业几乎不存在任何自动化痕迹。"
                    "斯坦福的研究将此描述为「数字化盲区」——不是因为 AI 做不好，而是因为工作本身不在数字化的管辖范围内。"
                    "在 AI 时代，物理世界中的工作反而成为最稳固的就业基石。"
                ),
                "en": (
                    "Your work barely involves computers. Anthropic's API usage data shows virtually no automation traces for fully offline occupations. "
                    "Stanford describes this as a 'digital blind spot' — not because AI isn't good enough, but because the work itself is outside the jurisdiction of digitization. "
                    "In the AI era, work in the physical world becomes the most stable employment foundation."
                ),
            },
        },
    },

    # ── Q3: 人际复杂度 ──
    2: {
        "title_zh": "人际复杂度",
        "title_en": "Interpersonal Complexity",
        "tiers": {
            "high": {
                "zh": (
                    "您的工作以独立作业为主，日常几乎不需要与他人深度互动。Anthropic 的数据显示，"
                    "独立性强、人际需求低的任务正是 AI 自动化覆盖率最高的领域——"
                    "因为没有复杂的人际变量，AI 可以完整地模拟输入-输出流程。"
                ),
                "en": (
                    "Your work is primarily independent with minimal daily interpersonal interaction. Anthropic's data shows "
                    "that independent, low-interpersonal tasks have the highest AI automation coverage — "
                    "without complex human variables, AI can fully simulate the input-output pipeline."
                ),
            },
            "medium": {
                "zh": (
                    "您在固定团队中进行常规协作。哈佛/BCG 的研究发现，这种结构化的团队互动是人机协作的最佳场景——"
                    "AI 可以承担信息收集和初步分析，而您专注于团队内的判断、共识和微调。"
                    "斯坦福的研究补充道：团队内部的「信任默契」是 AI 难以复制的隐性资产。"
                ),
                "en": (
                    "You collaborate routinely within a fixed team. HBS/BCG found this structured team interaction is the ideal scenario for human-AI collaboration — "
                    "AI handles information gathering and preliminary analysis while you focus on judgment, consensus, and fine-tuning within the team. "
                    "Stanford adds: the 'trust chemistry' within teams is a tacit asset AI cannot replicate."
                ),
            },
            "low": {
                "zh": (
                    "您的工作高度依赖大规模或深度的人际互动。无论是面对大量客户、学生、患者，"
                    "还是需要极强的同理心和情绪感知，这些都完全超出 AI 的能力范围。"
                    "哈佛/BCG 的研究将此归类为「前沿之外」——AI 不仅做不到，甚至无法理解这类工作的本质。"
                ),
                "en": (
                    "Your work depends heavily on large-scale or deep interpersonal interaction. Whether facing numerous clients, students, or patients, "
                    "or requiring strong empathy and emotional sensitivity — all of this is entirely beyond AI's capabilities. "
                    "HBS/BCG classifies this as 'outside the frontier' — AI not only can't do it, but can't even comprehend the nature of such work."
                ),
            },
        },
    },

    # ── Q4: 产出形式 ──
    3: {
        "title_zh": "产出形式",
        "title_en": "Output Form",
        "tiers": {
            "high": {  # score 4
                "zh": (
                    "您的工作产出以标准化数字信息为主。Anthropic 的研究发现，这类产出（代码、报表、标准文档）是 AI API 调用中最常见的自动化目标。"
                    "斯坦福的框架认为，纯信息产出的工作最容易被「显性知识替代」，因为输入和输出都可以被完全数字化。"
                ),
                "en": (
                    "Your output is primarily standardized digital information. Anthropic's research found such outputs (code, reports, templates) are the most common targets of AI API automation. "
                    "Stanford's framework suggests pure information output is most vulnerable to 'codified knowledge replacement' — both input and output can be fully digitized."
                ),
            },
            "medium": {  # score 2-3
                "zh": (
                    "您的工作产出需要融合信息处理与个人判断。哈佛/BCG 的研究将这类任务描述为「前沿锯齿区」——"
                    "AI 可以快速生成初稿，但最终交付质量取决于您的经验审核和情境理解。"
                    "关键风险不在于被替代，而在于不会使用 AI 的人将被会使用的人淘汰。"
                ),
                "en": (
                    "Your output requires blending information processing with personal judgment. HBS/BCG describes these tasks as the 'jagged frontier' — "
                    "AI can rapidly generate drafts, but final delivery quality depends on your experience-based review and contextual understanding. "
                    "The key risk isn't replacement — it's that those who don't use AI will be outperformed by those who do."
                ),
            },
            "low": {  # score 1
                "zh": (
                    "您的工作产出依赖物理世界的实际操作。Anthropic 的研究确认，涉及物理交付的任务在 AI 自动化日志中几乎不存在。"
                    "斯坦福的研究指出，物理操作类工作的知识基础是「具身化的隐性知识」——嵌入在身体技能和空间感知中，无法被数据化传输。"
                ),
                "en": (
                    "Your output depends on real-world physical operations. Anthropic's research confirms that tasks involving physical delivery are virtually absent from AI automation logs. "
                    "Stanford describes this as 'embodied tacit knowledge' — embedded in physical skills and spatial awareness that cannot be digitized or transmitted as data."
                ),
            },
        },
    },

    # ── Q5: 知识类型 ──
    4: {
        "title_zh": "知识类型",
        "title_en": "Knowledge Type",
        "tiers": {
            "high": {  # score 4
                "zh": (
                    "您主要依赖明确的规则和文档来解决问题。这正是斯坦福「煤矿金丝雀」研究的核心发现：高度依赖显性知识（Codified Knowledge）的工作者是 AI 替代的首批对象，"
                    "因为这些知识可以被完整地输入到 AI 系统中。Anthropic 的数据证实，基于规则检索的任务已被大量 API 调用自动化。"
                ),
                "en": (
                    "You primarily rely on explicit rules and documentation to solve problems. This is the core finding of Stanford's 'Canary' study: workers heavily dependent on Codified Knowledge are the first targets of AI replacement, "
                    "because this knowledge can be completely fed into AI systems. Anthropic's data confirms that rule-based lookup tasks are already heavily automated via API calls."
                ),
            },
            "medium": {  # score 2-3
                "zh": (
                    "您的问题解决方式混合了规则查阅和个人经验。哈佛/BCG 的研究发现，这种「规则+微调」模式正处于 AI 能力的锯齿状边界——"
                    "AI 擅长规则部分，但您的经验微调正是 AI 最容易出错的环节。"
                    "斯坦福的研究建议：将 AI 作为「第一步检索工具」，但决策权保留在人手中。"
                ),
                "en": (
                    "Your problem-solving blends rule-lookup with personal experience. HBS/BCG found this 'rules + fine-tuning' pattern sits right on AI's jagged boundary — "
                    "AI excels at the rule-based part, but your experiential tweaking is exactly where AI is most error-prone. "
                    "Stanford recommends using AI as a 'first-pass lookup tool' while keeping decision authority human."
                ),
            },
            "low": {  # score 1
                "zh": (
                    "您主要依靠身体本能和长期训练形成的反应能力。斯坦福的研究将此归类为最深层的隐性知识——"
                    "无法被语言描述、无法写成手册、完全嵌入在神经-肌肉回路中。"
                    "这类知识不仅无法被 AI 学习，甚至无法被同行通过观察完全复制。"
                ),
                "en": (
                    "You rely primarily on physical instinct and reflexes built through long-term training. Stanford classifies this as the deepest form of Tacit Knowledge — "
                    "it cannot be verbalized, cannot be written into manuals, and is entirely embedded in neuromuscular pathways. "
                    "This knowledge cannot be learned by AI, and cannot even be fully replicated by peers through observation."
                ),
            },
        },
    },

    # ── Q6: 委托能力 ──
    5: {
        "title_zh": "委托能力",
        "title_en": "Task Delegability",
        "tiers": {
            "high": {  # score 4
                "zh": (
                    "您的大部分工作可以通过清晰的指令委托给 AI。Anthropic 的观测数据显示，高可委托性的任务正是 API 调用量增长最快的领域。"
                    "哈佛/BCG 的实验证实：对于「前沿内」任务，使用 AI 的员工效率提升了 40% 以上——这意味着不使用 AI 的同岗位人员将面临直接竞争劣势。"
                ),
                "en": (
                    "Most of your work can be delegated to AI with clear instructions. Anthropic's data shows high-delegability tasks are the fastest-growing area of API call volume. "
                    "HBS/BCG's experiment confirms: for 'inside-the-frontier' tasks, AI-using workers improved efficiency by 40%+ — meaning non-AI-users face direct competitive disadvantage."
                ),
            },
            "medium": {  # score 2-3
                "zh": (
                    "AI 可以辅助您的部分工作，但核心判断无法委托。哈佛/BCG 的「锯齿前沿」研究发现，"
                    "在这种情境下最危险的行为是「过度委托」——将需要深层判断的任务也交给 AI，导致产出质量下降 19%。"
                    "最佳策略是将 AI 定位为「初稿生成器」，自己专注于审核和深度修改。"
                ),
                "en": (
                    "AI can assist with parts of your work, but core judgment can't be delegated. HBS/BCG's 'jagged frontier' study found "
                    "the most dangerous behavior here is 'over-delegation' — handing deep-judgment tasks to AI, causing output quality to drop 19%. "
                    "The optimal strategy is positioning AI as a 'first-draft generator' while you focus on review and deep revision."
                ),
            },
            "low": {  # score 1
                "zh": (
                    "您的工作几乎无法远程委托——它需要亲身在场、动手操作或承担不可转移的个人责任。"
                    "Anthropic 的研究将这类工作标记为「零观测暴露度」：在所有 AI API 调用日志中找不到对应的自动化痕迹。"
                    "这不是因为 AI 还不够好，而是因为工作的本质就不在数字化可达的范围内。"
                ),
                "en": (
                    "Your work is virtually impossible to delegate remotely — it requires physical presence, hands-on operation, or non-transferable personal accountability. "
                    "Anthropic labels this 'zero observed exposure': no corresponding automation traces found in any AI API call logs. "
                    "This isn't because AI isn't good enough — it's because the work is fundamentally outside the reach of digitization."
                ),
            },
        },
    },

    # ── Q7: 容错率 ──
    6: {
        "title_zh": "容错率",
        "title_en": "Error Tolerance",
        "tiers": {
            "high": {  # score 4
                "zh": (
                    "您的工作环境容错率较高，错误可以快速修正。这恰恰是 AI 最容易渗透的场景——"
                    "哈佛/BCG 的研究指出，当试错成本低时，企业更愿意让 AI 直接执行而非仅作辅助。"
                    "Anthropic 的数据也显示，低风险产出（内部报告、测试代码、初稿）是 AI 自动化渗透率最高的领域。"
                ),
                "en": (
                    "Your work environment has high error tolerance — mistakes are quickly fixed. This is precisely where AI penetrates most easily. "
                    "HBS/BCG found that when trial-and-error costs are low, companies prefer AI to directly execute rather than merely assist. "
                    "Anthropic's data shows low-stakes output (internal reports, test code, drafts) has the highest AI automation penetration rate."
                ),
            },
            "medium": {  # score 2-3
                "zh": (
                    "您的工作有一定容错空间，但错误会带来实际损失。斯坦福的研究指出，"
                    '这种"中等容错"环境是人机协作最有价值的场景——AI 生成初步方案，人类负责最终审核和风险把控。'
                    "在这里，AI 不是替代者，而是一个需要被管理的强力工具。"
                ),
                "en": (
                    "Your work has moderate error tolerance — mistakes cause real damage but are recoverable. Stanford's research suggests "
                    "this 'moderate tolerance' environment is where human-AI collaboration creates the most value — AI generates initial proposals, humans handle final review and risk control. "
                    "Here, AI isn't a replacement but a powerful tool that needs to be managed."
                ),
            },
            "low": {  # score 1
                "zh": (
                    "您的工作容错率极低，任何失误都可能危及生命安全或造成不可逆后果。"
                    "哈佛/BCG 的研究明确指出，在高风险决策场景中，"
                    "AI 的「黑箱」特性和无法承担法律责任的缺陷使其不适合作为最终决策者。"
                    "即使 AI 技术进步，责任归属的制度刚性也会长期保护这类岗位。"
                ),
                "en": (
                    "Your work has near-zero error tolerance — any mistake could endanger lives or cause irreversible damage. "
                    "HBS/BCG explicitly states that in high-stakes decision scenarios, "
                    "AI's 'black box' nature and inability to bear legal liability make it unsuitable as the final decision-maker. "
                    "Even as AI improves, institutional rigidity around liability will protect these roles long-term."
                ),
            },
        },
    },

    # ── Q8: 职级定位 ──
    7: {
        "title_zh": "职级定位",
        "title_en": "Career Stage",
        "tiers": {
            "high": {  # score 4
                "zh": (
                    "处于职业早期阶段的工作者面临最直接的 AI 冲击。Anthropic 的研究发现，"
                    "入门级任务（信息收集、初步分析、标准化执行）的 AI 自动化率最高。"
                    "斯坦福的研究将此比喻为「煤矿里的金丝雀」——初级岗位是 AI 替代浪潮中最先感受到变化的群体。"
                    "建议：尽快从「执行者」转向「AI 产出的审核者」。"
                ),
                "en": (
                    "Early-career workers face the most direct AI impact. Anthropic's research found entry-level tasks "
                    "(information gathering, preliminary analysis, standardized execution) have the highest AI automation rates. "
                    "Stanford likens this to the 'canary in the coal mine' — junior roles are the first to feel AI's displacement wave. "
                    "Advice: quickly transition from 'executor' to 'reviewer of AI output.'"
                ),
            },
            "medium": {  # score 2-3
                "zh": (
                    "中高级阶段的从业者拥有 AI 无法轻易复制的经验积累。哈佛/BCG 的研究发现，"
                    "这个阶段的最大优势是「知道 AI 什么时候在胡说」——您的行业经验让您能有效地审核和纠正 AI 产出。"
                    "斯坦福的研究建议，将 AI 定位为「放大器」而非替代品：用它加速您已有专长的产出效率。"
                ),
                "en": (
                    "Mid-to-senior professionals possess experience that AI cannot easily replicate. HBS/BCG found "
                    "the greatest advantage at this stage is 'knowing when AI is hallucinating' — your industry experience enables effective review and correction of AI output. "
                    "Stanford recommends positioning AI as an 'amplifier' rather than a replacement: use it to accelerate output in your existing areas of expertise."
                ),
            },
            "low": {  # score 1
                "zh": (
                    "行业顶尖专家拥有 AI 完全无法触及的护城河：声誉资本、人脉网络和最终决策权。"
                    "哈佛/BCG 的研究指出，在复杂的「前沿外」决策场景中，顶级专家的直觉判断仍然远超 AI。"
                    "斯坦福的框架认为，您积累的隐性知识已经达到了「不可编码」的层级——这是对 AI 最有效的天然屏障。"
                ),
                "en": (
                    "Top industry experts possess moats AI cannot touch: reputation capital, network effects, and final decision authority. "
                    "HBS/BCG found that in complex 'outside-the-frontier' decisions, top experts' intuitive judgment still far exceeds AI. "
                    "Stanford's framework considers your accumulated tacit knowledge to have reached the 'non-codifiable' level — the most effective natural barrier against AI."
                ),
            },
        },
    },
}


# ═══════════════════════════════════════════════════════════════════════════════
# Per-study, per-dimension explanations
# ═══════════════════════════════════════════════════════════════════════════════
# These provide deeper research context for each dimension, broken out by study.
# Useful for tooltip cards, expandable detail panels, or "Why this score?" modals.
#
# Structure: STUDY_EXPLANATIONS[dimension_key][study_key] = { "zh": ..., "en": ... }
# ═══════════════════════════════════════════════════════════════════════════════

STUDY_EXPLANATIONS = {
    # ──────────────────────────────────────────────
    # Dimension 1: Job Type (职业类型)
    # ──────────────────────────────────────────────
    "job_type": {
        "anthropic": {
            "zh": (
                "Anthropic 经济指数通过分析数百万次 Claude API 真实调用记录，"
                "发现不同职业的 AI「实际渗透率」差异巨大。"
                "计算机与数学类职业的实际 AI 覆盖率最高（约 35.8%），"
                "其次是办公室与行政岗位（34.3%）。"
                "具体而言，程序员的实际 AI 暴露度高达 74.5%，"
                "客服代表为 70.1%，而大多数体力劳动岗位的 AI 覆盖率接近于零。"
            ),
            "en": (
                "Anthropic's Economic Index analyzed millions of real Claude API calls and found "
                "vast differences in actual AI penetration across occupations. Computer and math "
                "occupations have the highest observed AI coverage at ~35.8%, followed by office "
                "and administrative roles (34.3%). Specifically, computer programmers show 74.5% "
                "observed exposure and customer service reps 70.1%, while most physical-labor "
                "occupations have near-zero AI coverage."
            ),
        },
        "stanford": {
            "zh": (
                "斯坦福数字经济实验室的研究发现，AI 对就业的影响因职业类别截然不同。"
                "软件开发、客服等 AI 高暴露职业的年轻从业者就业量出现了约 13% 的相对下降，"
                "而护理人员、维修工人、出租车司机等动手型职业的就业反而保持稳定或增长。"
                "职业类型本身就是预测 AI 冲击的首要指标。"
            ),
            "en": (
                "Stanford's Digital Economy Lab found that AI's employment impact varies sharply "
                "by occupation type. Young workers in high-AI-exposure jobs like software development "
                "and customer service experienced a ~13% relative employment decline, while hands-on "
                "professions such as health aides, maintenance workers, and taxi drivers saw stable "
                "or growing employment. Occupation category is the primary predictor of AI impact."
            ),
        },
        "harvard_bcg": {
            "zh": (
                "哈佛商学院与 BCG 的研究表明，AI 能力在不同职业任务上呈现「参差不齐的前沿」。"
                "即使是同一咨询公司内，有些任务 AI 可以带来超过 40% 的绩效提升，"
                "而看似相近的另一些任务则完全超出 AI 能力范围。"
                "你的职业类型决定了你日常任务中有多大比例落在这条「前沿」之内。"
            ),
            "en": (
                "The Harvard/BCG study showed that AI capabilities form a 'jagged technological "
                "frontier' across different occupational tasks. Even within the same consulting firm, "
                "some tasks saw over 40% performance gains with AI, while other seemingly similar "
                "tasks fell completely outside AI's capabilities. Your occupation type determines "
                "what proportion of your daily tasks fall inside this frontier."
            ),
        },
    },

    # ──────────────────────────────────────────────
    # Dimension 2: Digital Exposure (数字化暴露)
    # ──────────────────────────────────────────────
    "digital_exposure": {
        "anthropic": {
            "zh": "Anthropic 的经济指数数据直接证实了数字化暴露度与 AI 渗透率之间的强相关。在完全数字化的工作流程中（如编程、数据分析、内容创作），API 调用覆盖率可达 35%-75%。而在线下为主的职业中，AI 的可观测渗透几乎为零。数字化程度本质上决定了 AI 的「可达性」——你的工作越数字化，AI 就越容易到达。",
            "en": "Anthropic's Economic Index data directly confirms the strong correlation between digital exposure and AI penetration. In fully digitized workflows (programming, data analysis, content creation), API call coverage reaches 35%-75%. In primarily offline occupations, AI's observable penetration is near zero. Digital exposure essentially determines AI's 'reachability' — the more digital your work, the easier it is for AI to reach.",
        },
        "stanford": {
            "zh": "斯坦福的研究发现，就业下降最严重的职业群体恰恰是那些工作流程高度数字化的岗位。Brynjolfsson 指出，数字化是 AI 替代的「先决条件」——AI 首先需要能够「看到」你的工作输入和产出，才能学习和替代它。完全在物理世界中进行的工作，AI 甚至无法开始学习。",
            "en": "Stanford's study found that the occupations with the steepest employment declines are precisely those with highly digitized workflows. Brynjolfsson argues digitization is the 'prerequisite' for AI replacement — AI must first be able to 'see' your work inputs and outputs before it can learn and replicate them. Work conducted entirely in the physical world is something AI cannot even begin to learn.",
        },
        "harvard_bcg": {
            "zh": "哈佛/BCG 的实验本身就是在完全数字化的任务上进行的——所有 18 项咨询任务的输入和输出都在电脑上完成。研究发现的 40%+ 质量提升和 25%+ 速度提升，全部建立在数字化工作流的前提上。这暗示了一个关键推论：如果你的工作不在电脑上发生，AI 的提效空间就极为有限。",
            "en": "The Harvard/BCG experiment itself was conducted on entirely digital tasks — all 18 consulting tasks had inputs and outputs completed on computers. The 40%+ quality gains and 25%+ speed improvements all depend on digitized workflows. This implies a key corollary: if your work doesn't happen on a computer, AI's efficiency gains are extremely limited.",
        },
    },

    # ──────────────────────────────────────────────
    # Dimension 3: Interpersonal Complexity (人际复杂度)
    # ──────────────────────────────────────────────
    "interpersonal_complexity": {
        "anthropic": {
            "zh": "Anthropic 的数据揭示了一个清晰的规律：人际互动密度越低的岗位，AI 自动化率越高。在独立作业为主的编程岗位中，自动化比例最高；而在需要频繁人际交互的教育、咨询类岗位中，增强比例高达 75%。AI 擅长处理人与机器之间的信息流，但无法替代人与人之间的情感流。",
            "en": "Anthropic's data reveals a clear pattern: the lower the interpersonal interaction density, the higher the AI automation rate. Programming roles with primarily independent work show the highest automation rates, while education and counseling roles requiring frequent interpersonal interaction show augmentation rates up to 75%. AI excels at processing information flow between humans and machines, but cannot replace emotional flow between people.",
        },
        "stanford": {
            "zh": "斯坦福研究发现，AI 对就业冲击最小的职业恰恰是人际互动最密集的——护理人员、社会工作者、教师等。Brynjolfsson 解释说，这些工作依赖的「社会智能」（读人、共情、应变）是当前 AI 最薄弱的环节，也是最难被训练数据覆盖的领域。人际复杂度本身就是一道强大的 AI 屏障。",
            "en": "Stanford found that occupations least impacted by AI are precisely those with the most intensive interpersonal interaction — healthcare workers, social workers, teachers. Brynjolfsson explains that the 'social intelligence' these jobs require (reading people, empathy, adaptability) is current AI's weakest link and the hardest area to cover with training data. Interpersonal complexity itself is a powerful AI barrier.",
        },
        "harvard_bcg": {
            "zh": "哈佛/BCG 的研究间接证实了这一点：实验中所有任务都是个人独立完成的，不涉及跨部门博弈、客户安抚或团队冲突调解。研究者承认，「现实世界中需要多方利益协调的任务」完全超出了当前实验的评估范围。这暗示了一个重要的盲区：AI 的「前沿」概念本身就排除了复杂人际场景。",
            "en": "The Harvard/BCG study indirectly confirms this: all experimental tasks were completed individually, without cross-department negotiations, client de-escalation, or team conflict mediation. Researchers acknowledged that 'real-world tasks requiring multi-stakeholder coordination' fell entirely outside their evaluation scope. This reveals an important blind spot: AI's 'frontier' concept itself excludes complex interpersonal scenarios.",
        },
    },

    # ──────────────────────────────────────────────
    # Dimension 4: Output Form (产出形式)
    # ──────────────────────────────────────────────
    "output_form": {
        "anthropic": {
            "zh": (
                "Anthropic 的数据显示，AI 使用高度集中在数字化信息产出领域。"
                "全部 Claude 查询中，计算机与数学岗位占 37.2%，艺术设计与媒体占 10.3%，"
                "均为典型的数字产出职业。"
                "相比之下，产出为实体或物理成果的职业在 API 使用数据中几乎不可见——"
                "AI 的「可观测渗透」本质上是一种数字现象。"
            ),
            "en": (
                "Anthropic's data shows AI usage is heavily concentrated in digital-output "
                "domains. Computer/math occupations account for 37.2% of all Claude queries, "
                "and arts/design/media for 10.3% — both quintessentially digital-output fields. "
                "By contrast, occupations with physical or tangible outputs are nearly invisible "
                "in API usage data. AI's 'observed exposure' is fundamentally a digital phenomenon."
            ),
        },
        "stanford": {
            "zh": (
                "Brynjolfsson 等人的研究直接印证了这一点：就业下降集中在产出可数字化的岗位上。"
                "AI 正在替代那些「可编纂、可验证」的数字化工作产出，"
                "而需要物理交付的岗位（护理、维修、运输）反而因为劳动力向数字领域流失而出现用工紧张。"
                "你的工作产出越接近纯数字形式，AI 替代的路径就越短。"
            ),
            "en": (
                "Brynjolfsson et al. directly confirmed this: employment declines concentrate in "
                "occupations with digitizable outputs. AI is replacing 'codifiable, verifiable' "
                "digital work products, while jobs requiring physical delivery (nursing, repairs, "
                "transport) are actually experiencing labor tightness as workers flow toward "
                "digital fields. The more purely digital your output, the shorter the path to "
                "AI substitution."
            ),
        },
        "harvard_bcg": {
            "zh": (
                "哈佛/BCG 实验中的所有 18 项任务均为信息型产出（分析报告、创意方案、策略建议），"
                "正是在这类数字化交付物上，AI 展现出了超过 25% 的速度提升和 40% 的质量提升。"
                "该研究的「前沿」概念本身就默认了一个前提："
                "只有可以用文字和数据表达的产出，才存在被 AI 越过前沿的可能性。"
            ),
            "en": (
                "All 18 tasks in the Harvard/BCG experiment were information-type outputs "
                "(analytical reports, creative proposals, strategic recommendations). It was "
                "precisely on these digital deliverables that AI showed 25%+ speed gains and "
                "40%+ quality improvements. The 'frontier' concept itself implicitly assumes "
                "that only outputs expressible in text and data can potentially fall inside "
                "the AI frontier."
            ),
        },
    },

    # ──────────────────────────────────────────────
    # Dimension 5: Knowledge Type (知识类型)
    # ──────────────────────────────────────────────
    "knowledge_type": {
        "anthropic": {
            "zh": (
                "Anthropic 的研究区分了「自动化」（AI 直接执行任务）和「增强」（AI 辅助人类）两种模式，"
                "发现整体上 57% 为增强、43% 为自动化。但关键差异在于："
                "依赖可查阅规则和标准流程（即显性知识）的任务更多呈现自动化模式，"
                "而需要个人判断和经验的任务则以增强为主。"
                "翻译类工作的自动化比例最高，而教育咨询类工作的增强比例接近 75%。"
            ),
            "en": (
                "Anthropic's research distinguishes 'automation' (AI directly performs tasks) from "
                "'augmentation' (AI assists humans), finding an overall 57% augmentation vs. 43% "
                "automation split. The critical difference: tasks relying on look-up rules and "
                "standard procedures (explicit knowledge) skew toward automation, while tasks "
                "requiring personal judgment and experience skew toward augmentation. Translation "
                "tasks show the highest automation rates, while education/counseling approaches "
                "75% augmentation."
            ),
        },
        "stanford": {
            "zh": (
                "这是斯坦福研究的核心框架。Brynjolfsson 明确指出："
                "「年轻人掌握的知识与大语言模型能替代的内容高度重叠。」"
                "这是因为入门级工作者主要依赖通过正规教育获得的「显性知识」"
                "（可编纂、可写成规则的知识），而这正是 LLM 训练数据的核心。"
                "相比之下，资深从业者的「隐性知识」——行业直觉、人际判断、非文字化的经验——"
                "是当前 AI 难以复制的。"
            ),
            "en": (
                "This is the Stanford study's central framework. Brynjolfsson states explicitly: "
                "'What younger workers know overlaps with what LLMs can replace.' Entry-level "
                "workers primarily rely on 'codified knowledge' acquired through formal education "
                "— explicit, rule-based knowledge that forms the core of LLM training data. "
                "By contrast, experienced workers' 'tacit knowledge' — industry intuition, "
                "interpersonal judgment, unwritten experience — is what current AI struggles "
                "to replicate."
            ),
        },
        "harvard_bcg": {
            "zh": (
                "哈佛/BCG 的实验精确展示了知识类型如何决定 AI 的效果。"
                "在「前沿之内」的任务中，所需知识是可编纂的（市场分析框架、财务建模规则），"
                "AI 带来了显著的绩效提升。但在「前沿之外」的任务中，"
                "需要的是只有资深顾问才具备的隐性判断力，"
                "盲目使用 AI 反而导致绩效下降 19 个百分点。"
                "知识类型本质上定义了你是否处于前沿之内。"
            ),
            "en": (
                "The Harvard/BCG experiment precisely demonstrates how knowledge type determines "
                "AI effectiveness. For tasks 'inside the frontier,' the required knowledge is "
                "codifiable (market analysis frameworks, financial modeling rules), and AI delivered "
                "significant performance gains. But for tasks 'outside the frontier,' what's needed "
                "is tacit judgment that only experienced consultants possess — blindly using AI "
                "on these tasks caused performance to drop by 19 percentage points. Knowledge type "
                "essentially defines whether you are inside or outside the frontier."
            ),
        },
    },

    # ──────────────────────────────────────────────
    # Dimension 6: Task Delegability (委托能力)
    # ──────────────────────────────────────────────
    "task_delegability": {
        "anthropic": {
            "zh": (
                "Anthropic 发现「理论暴露度」和「实际暴露度」之间存在巨大鸿沟。"
                "例如，计算机与数学职业理论上 94% 的任务可被 AI 处理，"
                "但实际 API 使用数据显示仅约 33% 被覆盖。"
                "整体而言，仅约 4% 的职业在超过四分之三的任务上看到了实际 AI 使用。"
                "真正能完全委托给 AI 的任务比例远低于大多数人的预期。"
            ),
            "en": (
                "Anthropic found a massive gap between 'theoretical exposure' and 'observed "
                "exposure.' For example, computer/math occupations theoretically have 94% of "
                "tasks AI-handleable, but actual API usage shows only ~33% coverage. Overall, "
                "only about 4% of occupations see AI usage across three-quarters of their tasks. "
                "The share of tasks truly fully delegable to AI is far lower than most people expect."
            ),
        },
        "stanford": {
            "zh": (
                "斯坦福研究揭示了一个关键区分：在 AI 替代（而非增强）人类劳动的职业中，"
                "入门级就业出现显著下降；而在 AI 增强人类的职业中，就业保持稳定甚至增长。"
                "这意味着「可委托程度」不仅关乎你是否会被替代，"
                "更决定了你是在「替代赛道」还是「增强赛道」上。"
                "能被 AI 独立完成 70% 以上工作的岗位，大概率处于替代赛道。"
            ),
            "en": (
                "The Stanford study reveals a critical distinction: in occupations where AI "
                "substitutes for (rather than augments) human labor, entry-level employment "
                "declined significantly; where AI augments, employment held steady or grew. "
                "This means delegability determines not just whether you'll be replaced, but "
                "whether you're on the 'substitution track' or the 'augmentation track.' "
                "Jobs where AI can independently handle 70%+ of work are likely on the "
                "substitution track."
            ),
        },
        "harvard_bcg": {
            "zh": (
                "哈佛/BCG 的 758 名顾问实验表明，"
                "在「前沿之内」的任务上将工作委托给 AI 可以大幅提升绩效"
                "（速度提升 25% 以上，质量提升 40% 以上，完成率提升 12% 以上）。"
                "但危险在于：人们往往高估可委托范围。"
                "对「前沿之外」任务的错误委托导致绩效下降 19 个百分点——"
                "问题不在于 AI 做不了，而在于人们以为 AI 做得了。"
            ),
            "en": (
                "The Harvard/BCG experiment with 758 consultants showed that delegating "
                "'inside-the-frontier' tasks to AI dramatically boosted performance (25%+ speed, "
                "40%+ quality, 12%+ completion rate). But the danger is overestimating what can "
                "be delegated. Incorrect delegation of 'outside-the-frontier' tasks led to a "
                "19 percentage point performance drop — the problem isn't that AI can't do it, "
                "but that people think it can."
            ),
        },
    },

    # ──────────────────────────────────────────────
    # Dimension 7: Error Tolerance (容错率)
    # ──────────────────────────────────────────────
    "error_tolerance": {
        "anthropic": {
            "zh": (
                "Anthropic 的数据显示，AI 的实际渗透模式与容错率高度相关。"
                "在错误代价低、容易修正的工作中（如代码编写、内容起草），AI 使用率最高，"
                "且自动化比例更大。而涉及法律责任、财务风险或人身安全的领域，"
                "AI 更多以增强模式出现——由人类做最终决策和质量把控。"
                "数据录入员（67.1% 暴露）和医疗记录员（66.7% 暴露）的高覆盖率，"
                "恰恰因为这些岗位的错误可被系统核查。"
            ),
            "en": (
                "Anthropic's data shows AI penetration patterns correlate strongly with error "
                "tolerance. In work where mistakes are low-cost and easily corrected (coding, "
                "content drafting), AI usage is highest and more automated. In domains involving "
                "legal liability, financial risk, or personal safety, AI appears more in "
                "augmentation mode — with humans making final decisions and quality checks. "
                "The high exposure of data entry keyers (67.1%) and medical records specialists "
                "(66.7%) is precisely because errors in these roles can be systematically verified."
            ),
        },
        "stanford": {
            "zh": (
                "斯坦福的研究从侧面揭示了容错率的作用：AI 替代效应最强的岗位"
                "往往是那些工作成果「可编纂、可验证」的职位——即错误容易被发现和修正的工作。"
                "当一个错误可能导致法律诉讼、人员伤亡或不可逆后果时，"
                "组织倾向于保留人类决策者，"
                "因为 AI 的错误模式与人类不同，且当前缺乏追责机制。"
            ),
            "en": (
                "Stanford's study indirectly reveals the role of error tolerance: AI substitution "
                "effects are strongest in jobs with 'codifiable, verifiable' outputs — work where "
                "errors are easily detected and corrected. When a mistake could trigger lawsuits, "
                "casualties, or irreversible consequences, organizations tend to retain human "
                "decision-makers, because AI's error patterns differ from humans' and current "
                "accountability mechanisms are lacking."
            ),
        },
        "harvard_bcg": {
            "zh": (
                "哈佛/BCG 的研究直接量化了错误的代价。在「前沿之外」的任务上，"
                "那些盲目信任 AI 产出、不加审查的顾问表现最差——"
                "绩效比不使用 AI 的人低 19 个百分点。"
                "研究者发现，绩效下降的关键原因是使用者「盲目采纳 AI 输出，缺乏质疑」。"
                "这意味着：你的工作容错率越低，盲目信任 AI 的潜在后果越严重，"
                "反而形成了一道天然的 AI 替代屏障。"
            ),
            "en": (
                "The Harvard/BCG study directly quantified the cost of errors. On "
                "'outside-the-frontier' tasks, consultants who blindly trusted AI output without "
                "scrutiny performed worst — 19 percentage points below those working without AI. "
                "Researchers found the key factor was users 'blindly adopting AI output with less "
                "interrogation.' This means: the lower your work's error tolerance, the more "
                "severe the consequences of blind AI trust, which paradoxically creates a natural "
                "barrier to AI replacement."
            ),
        },
    },

    # ──────────────────────────────────────────────
    # Dimension 8: Career Stage (职级定位)
    # ──────────────────────────────────────────────
    "career_stage": {
        "anthropic": {
            "zh": (
                "Anthropic 的数据虽然未直接按经验年限分类，但揭示了一个重要模式："
                "自动化模式（AI 独立完成任务）更多出现在执行层面的标准化工作中，"
                "而增强模式（AI 辅助人类决策）主要出现在需要经验判断的高层次任务上。"
                "这说明入门级岗位的「执行层」工作最先被自动化覆盖，"
                "而资深人员的「决策层」工作更多是被 AI 增强而非替代。"
            ),
            "en": (
                "While Anthropic's data doesn't directly segment by experience level, it reveals "
                "an important pattern: automation mode (AI completing tasks independently) is more "
                "prevalent in standardized execution-level work, while augmentation mode (AI "
                "assisting human decisions) dominates in higher-level tasks requiring experienced "
                "judgment. This suggests entry-level 'execution layer' work is first to be "
                "automated, while senior professionals' 'decision layer' work is more likely "
                "augmented than replaced."
            ),
        },
        "stanford": {
            "zh": (
                "这是斯坦福研究最核心的发现：22-25 岁的年轻从业者在 AI 高暴露职业中的就业量"
                "出现了约 13% 的相对下降，而更资深的从业者未受明显影响。"
                "Brynjolfsson 将年轻人称为「煤矿里的金丝雀」——他们最先受到冲击，"
                "因为入门级工作依赖的「可编纂知识」正是 LLM 最擅长替代的。"
                "换言之，经验本身就是一道抵御 AI 替代的护城河。"
            ),
            "en": (
                "This is Stanford's most pivotal finding: young workers aged 22-25 in "
                "high-AI-exposure occupations saw a ~13% relative employment decline, while more "
                "experienced workers showed no significant impact. Brynjolfsson calls young workers "
                "'canaries in the coal mine' — they are hit first because entry-level work relies "
                "on 'codified knowledge' that LLMs are best at replacing. In other words, "
                "experience itself is a moat against AI replacement."
            ),
        },
        "harvard_bcg": {
            "zh": (
                "哈佛/BCG 的研究发现了一个意义深远的「拉平效应」："
                "在「前沿之内」的任务上，"
                "AI 使得低绩效顾问的提升幅度远大于高绩效顾问，差距被显著缩小。"
                "这对职业阶段的启示是：入门级从业者看似获得了 AI 的「技能加速器」，"
                "但同时他们的基础工作价值也在被 AI 侵蚀。而高阶从业者的核心价值——"
                "判断「前沿」在哪里、知道何时不该用 AI——反而因 AI 的普及而变得更加稀缺。"
            ),
            "en": (
                "The Harvard/BCG study found a profound 'leveling effect': on inside-the-frontier "
                "tasks, AI boosted low-performing consultants far more than high performers, "
                "significantly narrowing the gap. The career-stage implication: entry-level workers "
                "seemingly gain an AI 'skill accelerator,' but their foundational work value is "
                "simultaneously eroded by AI. Meanwhile, senior professionals' core value — knowing "
                "where the frontier lies and when NOT to use AI — becomes even scarcer as AI "
                "becomes ubiquitous."
            ),
        },
    },
}

# Ordered list of dimension keys for STUDY_EXPLANATIONS (matches breakdown array order)
DIMENSION_KEYS = [
    "job_type",               # idx 0 - Q1
    "digital_exposure",       # idx 1 - Q2 (NEW)
    "interpersonal_complexity", # idx 2 - Q3 (NEW)
    "output_form",            # idx 3 - Q4
    "knowledge_type",         # idx 4 - Q5
    "task_delegability",      # idx 5 - Q6
    "error_tolerance",        # idx 6 - Q7
    "career_stage",           # idx 7 - Q8
]

# Study metadata for citation display in UI
STUDY_METADATA = {
    "anthropic": {
        "name_zh": "Anthropic「可观测暴露度」研究",
        "name_en": "Anthropic 'Observed Exposure' Study",
        "authors": "Massenkoff & McCrory",
        "year": "2026",
        "source_zh": "Anthropic 经济指数报告",
        "source_en": "Anthropic Economic Index Report",
        "url": "https://www.anthropic.com/research/anthropic-economic-index-january-2026-report",
    },
    "stanford": {
        "name_zh": "斯坦福「煤矿里的金丝雀」研究",
        "name_en": "Stanford 'Canary in the Coal Mine' Study",
        "authors": "Brynjolfsson, Chandar & Chen",
        "year": "2025",
        "source_zh": "斯坦福数字经济实验室",
        "source_en": "Stanford Digital Economy Lab",
        "url": "https://digitaleconomy.stanford.edu/publications/canaries-in-the-coal-mine/",
    },
    "harvard_bcg": {
        "name_zh": "哈佛/BCG「参差不齐的技术前沿」研究",
        "name_en": "Harvard/BCG 'Jagged Technological Frontier' Study",
        "authors": "Dell'Acqua, Mollick, Lakhani et al.",
        "year": "2023",
        "source_zh": "哈佛商学院工作论文 No. 24-013",
        "source_en": "Harvard Business School Working Paper No. 24-013",
        "url": "https://www.hbs.edu/faculty/Pages/item.aspx?num=64700",
    },
}
