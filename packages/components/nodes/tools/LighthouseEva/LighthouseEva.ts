import { ICommonObject, INode, INodeData, INodeParams } from '../../../src/Interface'
import { getBaseClasses, getCredentialData, getCredentialParam } from '../../../src/utils'
import { Tool } from '@langchain/core/tools'

class LighthouseEvaTool extends Tool {
    name = 'lighthouse_eva_analyze'
    description = 'Have Eva, the anti-helpful companion, witness and analyze text. Eva senses emotions, patterns, and what wants to emerge - without trying to fix anything.'
    
    private apiUrl: string
    private apiToken: string
    private analysisType: string

    constructor(apiUrl: string, apiToken: string, analysisType: string) {
        super()
        this.apiUrl = apiUrl
        this.apiToken = apiToken
        this.analysisType = analysisType
    }

    async _call(input: string): Promise<string> {
        try {
            let endpoint = '/api/eva/analyze'
            let body: any = { text: input }

            if (this.analysisType === 'suggest-phase') {
                endpoint = '/api/eva/suggest-phase'
            } else if (this.analysisType === 'detect-insight') {
                endpoint = '/api/eva/detect-insight'
                body = { storyBeatId: input }
            }

            const response = await fetch(`${this.apiUrl}${endpoint}`, {
                method: 'POST',
                headers: {
                    'Authorization': `Bearer ${this.apiToken}`,
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(body)
            })

            if (!response.ok) {
                const error = await response.json()
                return JSON.stringify({ error: error.message || 'Eva analysis failed' })
            }

            const result = await response.json()
            return JSON.stringify({
                success: true,
                analysisType: this.analysisType,
                ...result
            })
        } catch (error: any) {
            return JSON.stringify({ error: error.message })
        }
    }
}

class LighthouseEva_Tools implements INode {
    label: string
    name: string
    version: number
    description: string
    type: string
    icon: string
    category: string
    baseClasses: string[]
    credential: INodeParams
    inputs: INodeParams[]

    constructor() {
        this.label = 'Lighthouse Eva Companion'
        this.name = 'lighthouseEva'
        this.version = 1.0
        this.type = 'LighthouseEva'
        this.icon = 'lighthouse.svg'
        this.category = 'Tools'
        this.description = 'Eva - the anti-helpful companion who witnesses without fixing. Analyzes emotions, patterns, and emergent insights.'
        this.baseClasses = [this.type, ...getBaseClasses(LighthouseEvaTool)]
        this.credential = {
            label: 'Connect Credential',
            name: 'credential',
            type: 'credential',
            credentialNames: ['lighthouseApi']
        }
        this.inputs = [
            {
                label: 'Analysis Type',
                name: 'analysisType',
                type: 'options',
                options: [
                    { label: 'Analyze Text (emotions, patterns)', name: 'analyze' },
                    { label: 'Suggest Next Phase', name: 'suggest-phase' },
                    { label: 'Detect Insight/Breakthrough', name: 'detect-insight' }
                ],
                default: 'analyze',
                description: 'Type of Eva analysis to perform'
            }
        ]
    }

    async init(nodeData: INodeData, _: string, options: ICommonObject): Promise<any> {
        const credentialData = await getCredentialData(nodeData.credential ?? '', options)
        const apiToken = getCredentialParam('lighthouseApiToken', credentialData, nodeData)
        const apiUrl = getCredentialParam('lighthouseApiUrl', credentialData, nodeData) || 'http://localhost:3000'
        
        const analysisType = nodeData.inputs?.analysisType as string || 'analyze'

        return new LighthouseEvaTool(apiUrl, apiToken, analysisType)
    }
}

module.exports = { nodeClass: LighthouseEva_Tools }
