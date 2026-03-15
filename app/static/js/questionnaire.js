document.addEventListener('alpine:init', () => {
    Alpine.data('quiz', () => ({
        // Data from server
        jobs: window.__QUIZ_DATA__.jobs,
        jobGroups: window.__QUIZ_DATA__.jobGroups,
        questions: window.__QUIZ_DATA__.questions,

        // State
        currentStep: 0,       // 0 = Q1 (job), 1-5 = Q2-Q6, 6 = submitting
        answers: {},           // { q1: jobId, q2: 'A', q3: 'B', ... }
        selectedJob: null,
        searchQuery: '',
        transitioning: false,

        // Computed
        get totalSteps() { return 6; },

        get progress() {
            return Math.round((this.currentStep / this.totalSteps) * 100);
        },

        get progressText() {
            return `${this.currentStep + 1} / ${this.totalSteps}`;
        },

        get canGoBack() { return this.currentStep > 0; },

        // Job filtering
        filteredJobs(groupId) {
            const groupJobs = this.jobs.filter(j => j.group === groupId);
            if (!this.searchQuery.trim()) return groupJobs;
            const q = this.searchQuery.toLowerCase().trim();
            return groupJobs.filter(j =>
                j.name_zh.toLowerCase().includes(q) ||
                j.name_en.toLowerCase().includes(q) ||
                j.id.toLowerCase().includes(q)
            );
        },

        hasJobsInGroup(groupId) {
            return this.filteredJobs(groupId).length > 0;
        },

        // Actions
        selectJob(job) {
            this.selectedJob = job;
            this.answers.q1 = job.id;
            setTimeout(() => this.goNext(), 400);
        },

        selectOption(qIdx, opt) {
            const key = `q${qIdx + 2}`;
            this.answers[key] = opt.label;
            setTimeout(() => this.goNext(), 400);
        },

        isOptionSelected(qIdx, label) {
            return this.answers[`q${qIdx + 2}`] === label;
        },

        goNext() {
            if (this.transitioning) return;
            if (this.currentStep < 5) {
                this.transitioning = true;
                setTimeout(() => {
                    this.currentStep++;
                    this.transitioning = false;
                }, 50);
            } else {
                this.submit();
            }
        },

        goBack() {
            if (this.transitioning || this.currentStep === 0) return;
            this.transitioning = true;
            setTimeout(() => {
                this.currentStep--;
                this.transitioning = false;
            }, 50);
        },

        async submit() {
            this.currentStep = 6;
            const payload = {
                job_id: this.answers.q1,
                q2: this.answers.q2,
                q3: this.answers.q3,
                q4: this.answers.q4,
                q5: this.answers.q5,
                q6: this.answers.q6,
            };

            try {
                const resp = await fetch('/api/score', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(payload),
                });
                const data = await resp.json();
                sessionStorage.setItem('quizResult', JSON.stringify(data));
                window.location.href = '/result';
            } catch (err) {
                console.error('Submit error:', err);
                this.currentStep = 5;
            }
        },
    }));
});
