import { ICommonObject, INode, INodeData, INodeParams } from '../../../src/Interface'
import { getBaseClasses, getCredentialData, getCredentialParam } from '../../../src/utils'
import { Tool } from '@langchain/core/tools'

interface StoryBeatInput {
    phase: 'yellow' | 'violet' | 'white-gold' | 'emerald'
    text: string
    color?: string
    sound?: string
    shared?: boolean
}

class LighthouseStoryBeatTool extends Tool {
    name = 'lighthouse_story_beat'
    description = 'Create or retrieve story beats from Lighthouse healing platform. Phases: yellow (inquiry), violet (reflection), white-gold (insight), emerald (commitment)'
    
    private apiUrl: string
    private apiToken: string
    private action: string
    private defaultPhase: string

    constructor(apiUrl: string, apiToken: string, action: string, defaultPhase: string) {
        super()
        this.apiUrl = apiUrl
        this.apiToken = apiToken
        this.action = action
        this.defaultPhase = defaultPhase
    }

    async _call(input: string): Promise<string> {
        try {
            if (this.action === 'create') {
                // Parse input - expected format: "phase: <phase>, text: <text>" or just text
                let phase = this.defaultPhase
                let text = input
                
                const phaseMatch = input.match(/phase:\s*(yellow|violet|white-gold|emerald)/i)
                if (phaseMatch) {
                    phase = phaseMatch[1].toLowerCase()
                    text = input.replace(/phase:\s*(yellow|violet|white-gold|emerald),?\s*/i, '').trim()
                }

                const response = await fetch(`${this.apiUrl}/api/story-beats`, {
                    method: 'POST',
                    headers: {
                        'Authorization': `Bearer ${this.apiToken}`,
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({
                        phase,
                        text,
                        shared: false
                    })
                })

                if (!response.ok) {
                    const error = await response.json()
                    return JSON.stringify({ error: error.message || 'Failed to create story beat' })
                }

                const beat = await response.json()
                return JSON.stringify({
                    success: true,
                    beatId: beat.id,
                    phase: beat.phase,
                    message: `Story beat created in ${phase} phase`
                })
            } else {
                // Get story beats
                const response = await fetch(`${this.apiUrl}/api/story-beats`, {
                    method: 'GET',
                    headers: {
                        'Authorization': `Bearer ${this.apiToken}`,
                        'Content-Type': 'application/json'
                    }
                })

                if (!response.ok) {
                    const error = await response.json()
                    return JSON.stringify({ error: error.message || 'Failed to retrieve story beats' })
                }

                const beats = await response.json()
                return JSON.stringify({
                    success: true,
                    count: beats.length,
                    beats: beats.slice(0, 10).map((b: any) => ({
                        id: b.id,
                        phase: b.phase,
                        text: b.text?.substring(0, 100) + (b.text?.length > 100 ? '...' : ''),
                        createdAt: b.created_at
                    }))
                })
            }
        } catch (error: any) {
            return JSON.stringify({ error: error.message })
        }
    }
}

class LighthouseStoryBeat_Tools implements INode {
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
        this.label = 'Lighthouse Story Beat'
        this.name = 'lighthouseStoryBeat'
        this.version = 1.0
        this.type = 'LighthouseStoryBeat'
        this.icon = 'lighthouse.svg'
        this.category = 'Tools'
        this.description = 'Create or retrieve story beats from Lighthouse ceremonial storytelling platform'
        this.baseClasses = [this.type, ...getBaseClasses(LighthouseStoryBeatTool)]
        this.credential = {
            label: 'Connect Credential',
            name: 'credential',
            type: 'credential',
            credentialNames: ['lighthouseApi']
        }
        this.inputs = [
            {
                label: 'Action',
                name: 'action',
                type: 'options',
                options: [
                    { label: 'Create Story Beat', name: 'create' },
                    { label: 'Get Story Beats', name: 'get' }
                ],
                default: 'create',
                description: 'Action to perform'
            },
            {
                label: 'Default Phase',
                name: 'defaultPhase',
                type: 'options',
                options: [
                    { label: '🟨 Yellow (Inquiry)', name: 'yellow' },
                    { label: '💜 Violet (Reflection)', name: 'violet' },
                    { label: '✨ White-Gold (Insight)', name: 'white-gold' },
                    { label: '💚 Emerald (Commitment)', name: 'emerald' }
                ],
                default: 'yellow',
                description: 'Default narrative phase if not specified in input',
                additionalParams: true,
                optional: true
            }
        ]
    }

    async init(nodeData: INodeData, _: string, options: ICommonObject): Promise<any> {
        const credentialData = await getCredentialData(nodeData.credential ?? '', options)
        const apiToken = getCredentialParam('lighthouseApiToken', credentialData, nodeData)
        const apiUrl = getCredentialParam('lighthouseApiUrl', credentialData, nodeData) || 'http://localhost:3000'
        
        const action = nodeData.inputs?.action as string || 'create'
        const defaultPhase = nodeData.inputs?.defaultPhase as string || 'yellow'

        return new LighthouseStoryBeatTool(apiUrl, apiToken, action, defaultPhase)
    }
}

module.exports = { nodeClass: LighthouseStoryBeat_Tools }
