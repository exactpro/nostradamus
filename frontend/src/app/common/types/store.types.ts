import { CommonStore } from 'app/common/store/common/types';
import { QAMetricsStore } from 'app/common/store/qa-metrics/types';
import { AuthStore } from 'app/common/store/auth/types';
import { SettingsStore } from 'app/common/store/settings/types';
import { VirtualAssistantStore } from 'app/common/store/virtual-assistant/types';
import { ToastStore } from 'app/modules/toasts-overlay/store/types';
import { SettingTrainingStore } from 'app/modules/settings/fields/settings_training/store/types';

export interface RootStore {
	toasts: ToastStore,
	auth: AuthStore,
	settings: {
		settingsStore: SettingsStore,
		settingsTrainingStore: SettingTrainingStore
	}
	virtualAssistant: VirtualAssistantStore,
	qaMetricsPage: QAMetricsStore,
	common: CommonStore
}
