export enum SenderType {
  system = "system",
  user = "user",
}

export type Message = {
  text: string,
  sender: SenderType
}

export type Conversation = {
  id: number,
  title: string,
  messages: Message[]
}