import { ICommonObject, INode, INodeData, INodeParams } from '../../../src/Interface'

class PromptDecomposition_Agentflow implements INode {
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
        this.label = 'Prompt Decomposition'
        this.name = 'promptDecompositionAgentflow'
        this.version = 1.0
        this.type = 'PromptDecomposition'
        this.category = 'Agent Flows'
        this.description =
            'Decompose a prompt through Four Directions (Medicine Wheel): EAST(Vision), SOUTH(Analysis), WEST(Validation), NORTH(Action). Produces a dependency-ordered action stack.'
        this.baseClasses = [this.type]
        this.color = '#8B5CF6'
        this.tags = ['Relational Intelligence', 'Medicine Wheel', 'PDE']
        this.inputs = [
            {
                label: 'Prompt',
                name: 'prompt',
                type: 'string',
                rows: 4,
                placeholder: 'Enter the prompt to decompose...',
                description: 'The prompt to decompose through Four Directions analysis'
            },
            {
                label: 'Output Format',
                name: 'outputFormat',
                type: 'options',
                options: [
                    { label: 'JSON', name: 'json' },
                    { label: 'Markdown', name: 'markdown' },
                    { label: 'Action Stack Only', name: 'actionStack' }
                ],
                default: 'json',
                description: 'Format for the decomposition output'
            },
            {
                label: 'Include Implicit Intents',
                name: 'includeImplicit',
                type: 'boolean',
                default: true,
                optional: true,
                description: 'Extract hidden/implicit requirements from the prompt'
            },
            {
                label: 'Max Actions',
                name: 'maxActions',
                type: 'number',
                default: 20,
                optional: true,
                description: 'Maximum number of actions in the stack'
            },
            {
                label: 'Ceremony Threshold',
                name: 'ceremonyThreshold',
                type: 'number',
                default: 0.3,
                optional: true,
                step: 0.1,
                description:
                    'Minimum spiritual+emotional coverage to proceed without ceremony (0-1). Lower = more sensitive.'
            }
        ]
    }

    async run(nodeData: INodeData, _input: string, _options?: ICommonObject): Promise<any> {
        const prompt = nodeData.inputs?.prompt as string
        const outputFormat = (nodeData.inputs?.outputFormat as string) || 'json'
        const includeImplicit = nodeData.inputs?.includeImplicit !== false
        const maxActions = (nodeData.inputs?.maxActions as number) || 20
        const ceremonyThreshold = (nodeData.inputs?.ceremonyThreshold as number) || 0.3

        if (!prompt) {
            throw new Error('Prompt is required for decomposition')
        }

        // Dynamic import to allow package to be optional
        let pdeModule: any
        try {
            pdeModule = await import('ava-langchain-prompt-decomposition')
        } catch {
            throw new Error(
                'ava-langchain-prompt-decomposition is not installed. ' +
                'Install it with: npm install ava-langchain-prompt-decomposition'
            )
        }

        const {
            DirectionalDecomposer,
            IntentExtractor,
            DependencyMapper,
            ActionStackBuilder,
            MedicineWheelBridge
        } = pdeModule

        const decomposer = new DirectionalDecomposer()
        const extractor = new IntentExtractor({ extractImplicit: includeImplicit })
        const mapper = new DependencyMapper()
        const builder = new ActionStackBuilder({ includeImplicit, maxItems: maxActions })
        const bridge = new MedicineWheelBridge({ ceremonyThreshold })

        const directionalAnalysis = decomposer.decompose(prompt)
        const intentResult = await extractor.extract(prompt)
        const graph = mapper.buildGraph(intentResult.secondary)
        const order = mapper.computeExecutionOrder(graph)
        const decomposition = builder.build(directionalAnalysis, intentResult, order)
        const wheelEnriched = bridge.enrich(directionalAnalysis)

        // Build output based on format
        let output: any

        switch (outputFormat) {
            case 'markdown':
                output = builder.toMarkdown(decomposition)
                break
            case 'actionStack':
                output = decomposition.actionStack
                break
            case 'json':
            default:
                output = decomposition
                break
        }

        const state = (nodeData as any).state || {}

        return {
            id: nodeData.id,
            name: this.name,
            input: { prompt },
            output: {
                decomposition: output,
                balance: decomposition.balance,
                leadDirection: decomposition.leadDirection,
                neglectedDirections: decomposition.neglectedDirections,
                ceremonyRequired: wheelEnriched.ceremonyRequired,
                relationalCoverage: wheelEnriched.relationalCoverage,
                actionCount: decomposition.actionStack.length,
                primaryIntent: decomposition.primary
            },
            state
        }
    }
}

module.exports = { nodeClass: PromptDecomposition_Agentflow }
