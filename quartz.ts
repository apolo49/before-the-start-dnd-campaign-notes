import { loadQuartzConfig, loadQuartzLayout } from "./quartz/plugins/loader/config-loader"
import * as Component from "./quartz/components"

const config = await loadQuartzConfig()
export default config
export const layout = await loadQuartzLayout({
    byPageType: {
        content: {
            right: [Component.RandomPageButton()]
        },
    }
})