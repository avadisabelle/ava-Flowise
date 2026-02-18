import { ICommonObject, INode, INodeData, INodeParams } from '../../../src/Interface'

class MedicineWheelGate_Agentflow implements INode {
    label: string
    name: string
    version: number
    description: string
    type: string
    icon: string
    category: string
    color: string
    tags: string[]
    baseClasses: string[]
    inputs: INodeParams[]

    constructor() {
        this.label = 'Medicine Wheel Gate'
        this.name = 'medicineWheelGateAgentflow'
        this.version = 1.0
        this.type = 'MedicineWheelGate'
        this.category = 'Agent Flows'
        this.description =
            'Relational accountability gate using Medicine Wheel assessment. Checks balance across four directions and ceremony requirements before allowing flow to proceed.'
        this.baseClasses = [this.type]
        this.color = '#F59E0B'
        this.tags = ['Relational Intelligence', 'Medicine Wheel', 'Gate']
        this.inputs = [
            {
                label: 'Input Text',
                name: 'inputText',
                type: 'string',
                rows: 4,
                placeholder: 'Text or prompt to assess through the Medicine Wheel...',
                description: 'The text to assess for relational balance'
            },
            {
                label: 'Gate Mode',
                name: 'gateMode',
                type: 'options',
                options: [
                    { label: 'Advisory (warn but proceed)', name: 'advisory' },
                    { label: 'Enforce (halt if unbalanced)', name: 'enforce' }
                ],
                default: 'advisory',
                description: 'Whether to halt flow or just warn when ceremony is needed'
            },
            {
                label: 'Balance Threshold',
                name: 'balanceThreshold',
                type: 'number',
                default: 0.4,
                optional: true,
                step: 0.1,
                description: 'Minimum directional balance to proceed without caution (0-1)'
            },
            {
                label: 'Neglect Threshold',
                name: 'neglectThreshold',
                type: 'number',
                default: 0.15,
                optional: true,
                step: 0.05,
                description: 'Below this proportion, a quadrant is considered neglected (0-1)'
            },
            {
                label: 'Include Guidance',
                name: 'includeGuidance',
                type: 'boolean',
                default: true,
                optional: true,
                description: 'Include relational guidance messages in output'
            }
        ]
    }

    async run(nodeData: INodeData, _input: string, _options?: ICommonObject): Promise<any> {
        const inputText = nodeData.inputs?.inputText as string
        const gateMode = (nodeData.inputs?.gateMode as string) || 'advisory'
        const balanceThreshold = (nodeData.inputs?.balanceThreshold as number) || 0.4
        const neglectThreshold = (nodeData.inputs?.neglectThreshold as number) || 0.15
        const includeGuidance = nodeData.inputs?.includeGuidance !== false

        if (!inputText) {
            throw new Error('Input text is required for Medicine Wheel assessment')
        }

        const {
            DirectionalDecomposer,
            MedicineWheelBridge
        } = await import('ava-langchain-prompt-decomposition')

        const decomposer = new DirectionalDecomposer({ neglectThreshold, balanceThreshold })
        const bridge = new MedicineWheelBridge({ ceremonyThreshold: balanceThreshold })

        const analysis = decomposer.decompose(inputText)
        const enriched = bridge.enrich(analysis)
        const guidance = includeGuidance ? bridge.getRelationalGuidance(analysis) : []

        // Determine gate decision
        const canProceed = gateMode === 'advisory' || !enriched.ceremonyRequired
        const decision = enriched.ceremonyRequired
            ? gateMode === 'enforce'
                ? 'HOLD'
                : 'CAUTION'
            : 'PROCEED'

        const state = (nodeData as any).state || {}

        return {
            id: nodeData.id,
            name: this.name,
            input: { inputText },
            output: {
                decision,
                canProceed,
                balance: analysis.balance,
                leadDirection: analysis.leadDirection,
                neglectedDirections: analysis.neglectedDirections,
                ceremonyRequired: enriched.ceremonyRequired,
                relationalCoverage: enriched.relationalCoverage,
                quadrantPresence: enriched.quadrantPresence,
                guidance,
                directionCounts: {
                    east: analysis.directions.east?.length ?? 0,
                    south: analysis.directions.south?.length ?? 0,
                    west: analysis.directions.west?.length ?? 0,
                    north: analysis.directions.north?.length ?? 0
                }
            },
            state
        }
    }
}

module.exports = { nodeClass: MedicineWheelGate_Agentflow }
