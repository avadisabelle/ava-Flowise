import { INodeParams, INodeCredential } from '../src/Interface'

class LighthouseApi implements INodeCredential {
    label: string
    name: string
    version: number
    description: string
    inputs: INodeParams[]

    constructor() {
        this.label = 'Lighthouse API'
        this.name = 'lighthouseApi'
        this.version = 1.0
        this.description = 'Lighthouse STPB - Ceremonial storytelling platform for healing journeys'
        this.inputs = [
            {
                label: 'API Token',
                name: 'lighthouseApiToken',
                type: 'password',
                description: 'Bearer token for Lighthouse API authentication'
            },
            {
                label: 'API URL',
                name: 'lighthouseApiUrl',
                type: 'string',
                default: 'http://localhost:3000',
                description: 'Base URL for Lighthouse API (e.g., https://your-stpb-app.vercel.app)'
            }
        ]
    }
}

module.exports = { credClass: LighthouseApi }
