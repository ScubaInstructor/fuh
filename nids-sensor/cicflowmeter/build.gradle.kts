plugins {
    id("java")
    kotlin("jvm") version "2.1.0"
    id("application")
}

application {
    mainClass.set("com.vanwaasen.cicfm.KafkaFlowmeterKt")
}

tasks.named<JavaExec>("run") {
    args = listOf("--config=config/kafkacicflowmeter.yml")
}

group = "com.vanwaasen.cicfm"
version = "1.0"

java {
    sourceCompatibility = JavaVersion.VERSION_11
    targetCompatibility = JavaVersion.VERSION_11
    toolchain {
        languageVersion.set(JavaLanguageVersion.of(11))
    }
}

kotlin {
    jvmToolchain(11)
}

repositories {
    mavenCentral()
}

dependencies {

    implementation("com.fasterxml.jackson.core:jackson-databind:2.18.2")
    implementation("com.fasterxml.jackson.module:jackson-module-kotlin:2.18.2")
    implementation("com.fasterxml.jackson.dataformat:jackson-dataformat-yaml:2.18.2")

    implementation("org.apache.commons:commons-math3:3.5")
    implementation("org.apache.commons:commons-lang3:3.6")
    implementation("org.apache.tika:tika-core:2.9.2")
}


tasks.register<Jar>("fatJar") {
    archiveBaseName.set("kafka-cic-flowmeter")
    archiveVersion.set("1.2.0")
    duplicatesStrategy = DuplicatesStrategy.EXCLUDE

    manifest {
        attributes["Main-Class"] = ""
    }

    from(
        configurations.runtimeClasspath.get().filter { it.exists() }
            .map { if (it.isDirectory) it else zipTree(it) }
    )

    with(tasks.jar.get())
}