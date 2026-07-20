use std::time::SystemTime;

#[derive(Clone, Debug, Default)]
pub struct UsageSection {
    pub percentage: f64,
    pub resets_at: Option<SystemTime>,
}

#[derive(Clone, Debug, Default)]
pub struct UsageData {
    pub session: UsageSection,
    pub weekly: UsageSection,
    /// Weekly limit scoped to a specific model (e.g. Fable). Only some
    /// Claude subscription plans expose this; `None` when absent.
    pub weekly_scoped: Option<ScopedUsage>,
}

/// A usage limit tied to a particular model, surfaced as a colored underlay
/// on the weekly bar.
#[derive(Clone, Debug, Default)]
pub struct ScopedUsage {
    pub model_name: String,
    pub section: UsageSection,
}

#[derive(Clone, Debug, Default)]
pub struct AppUsageData {
    pub claude_code: Option<UsageData>,
    pub codex: Option<UsageData>,
    pub antigravity: Option<UsageData>,
}
