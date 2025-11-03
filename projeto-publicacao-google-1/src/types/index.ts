// Este arquivo exporta tipos e interfaces utilizados em toda a aplicação

export interface Config {
    googleApiKey: string;
    projectId: string;
}

export interface PublishResponse {
    success: boolean;
    message: string;
    data?: any;
}