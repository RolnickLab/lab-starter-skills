# Design Patterns & Antipatterns

## Recommended Patterns
*   **Strategy:** Select an algorithm at runtime. Essential for OCP.
*   **Factory/Builder:** Decouple complex object creation from the consumer.
*   **Observer:** Decouple event producers from consumers. Basis for reactive systems.
*   **Adapter:** Map incompatible interfaces. Essential for Clean Architecture (Adapters layer).
*   **Decorator:** Dynamically add responsibilities to an object without subclassing.

## Antipatterns to Avoid
*   **Singleton:** Global state in disguise. Makes testing and concurrency difficult.
*   **God Object:** A class that knows too much or does too much. Violates SRP.
*   **Golden Hammer:** Overusing a familiar technology (e.g., using a DB as a message queue).
*   **Poltergeists:** Short-lived, useless classes used only to invoke one other class.
*   **Soft Coding:** Moving too much logic into config files (making it un-debuggable).

## Selection Rule
A pattern is only valid if it simplifies the system or solves a clear design problem. If it adds complexity without a quantifiable benefit (e.g., testability, scalability), reject it.
